#!/usr/bin/env python3

from cbapi.response import *
from cbapi.psc.defense import *
from argparse import ArgumentParser
from time import sleep


def get_cb_session(profile):
    psc = 1
    try:
        cb = CbDefenseAPI(profile=profile)
    except:
        psc = 0
        cb = CbResponseAPI(profile=profile)
    return cb, psc


def process_hostname(cb, hostname, psc):

    sensors = set()
    # Query Cb for sensor by hostname, add to sensors
    if psc:
        try:
            sensors.add(
                cb.select(Device).where('hostNameExact:'+hostname).first()
            )
        except:
            sensors.add(
                cb.select(Device).where('hostName:'+hostname).first()
            )
    else:
        sensors.add(cb.select(Sensor).where('hostname:'+hostname).first())
    return sensors


def process_hostname_file(cb, hostname_path, psc):

    # Read in hostnames from file
    with open(hostname_path) as h:
        hostnames = h.read().splitlines()
    sensors = set()
    # Query Cb for each sensor by hostname, add to sensors
    if psc:
        for hostname in hostnames:
            sensors.add(cb.select(Device).where('hostName:'+hostname).first())
    else:
        for hostname in hostnames:
            sensors.add(cb.select(Sensor).where('hostname:'+hostname).first())
    return sensors


def enumerate_directory(host, directory, filename):
    """
    Enumerates directory on host, returns existence of filename
    """
    dir = host.list_directory(directory)
    file_exists = 0
    for file in dir:
        if str.lower(file['filename']) == str.lower(filename):
            file_exists = 1
    return file_exists


def start_process(session, process, working_directory='C:\\Temp\\'):
    p = session.create_process(
        process,
        wait_for_output=True,
        working_directory=working_directory,
        wait_timeout=300)

    return str(p, 'utf-8')


def start_capture(
    session,
    sensor,
    comp_name,
    parent_directory,
    working_directory,
    file_name
):

    trace_exists = enumerate_directory(
        session,
        parent_directory + working_directory,
        file_name + '.etl'
    )

    if trace_exists:
        session.delete_file(
            parent_directory + working_directory + file_name + '.etl')

    # Print hostname and output for each host
    print(comp_name + ':')

    print(start_process(
        session,
        """cmd /c \"netsh trace start capture=yes traceFile="""
        + parent_directory + working_directory + file_name + """.etl\"""",
        # parent_directory + working_directory + start_capture,
        parent_directory + working_directory
        )
    )


def end_capture(session, parent_directory, working_directory, file_name):
    print(start_process(
        session,
        """cmd /c \"netsh trace stop\"""",
        # parent_directory + working_directory + end_capture,
        parent_directory + working_directory
        )
    )

    cab_exists = 0
    while not cab_exists:

        cab_exists = enumerate_directory(
            session,
            parent_directory + working_directory,
            file_name + '.cab'
        )
        sleep(15)


def create_working_directory(session, parent_directory, working_directory):
    dir_exists = enumerate_directory(
        session,
        parent_directory,
        working_directory.rstrip('\\')
    )
    # If working_directory does not exist, create it
    if not dir_exists:
        session.create_directory(parent_directory + working_directory)
    return dir_exists


def cleanup_and_return(
    session,
    sensor,
    comp_name,
    dir_exists,
    parent_directory,
    working_directory,
    file_name
):

    with open(comp_name + file_name + '.etl', 'wb+') as n:
        n.write(session.get_file(
            parent_directory + working_directory + file_name + '.etl'))

    # Clean up, clean up, everybody everywhere
    session.delete_file(
        parent_directory + working_directory
        + file_name + '.cab'
    )
    session.delete_file(
        parent_directory + working_directory
        + file_name + '.etl'
    )

    # If working_directory was created earlier, delete it
    if not dir_exists:
        session.delete_file(parent_directory + working_directory)


def capture_packets(hostname, hostname_path, profile, capture_time):
    """
    Captures packets from remote host, returns as etl file
    """

    FILE_NAME = 'NetworkTrace'
    PARENT_DIRECTORY = 'C:\\'
    WORKING_DIRECTORY = 'Temp\\'

    cb, psc = get_cb_session(profile)

    if hostname:
        sensors = process_hostname(cb, hostname, psc)
    else:
        sensors = process_hostname_file(cb, hostname_path, psc)

    # Push scripts to each sensor, execute, then cleanup
    for sensor in sensors:

        if psc:
            comp_name = str(sensor.name)
        else:
            comp_name = str(sensor.computer_name)
        comp_name = comp_name[comp_name.find("\\")+1:]

        # Establish Live Response session for the sensor
        with sensor.lr_session() as session:

            dir_exists = create_working_directory(
                session,
                PARENT_DIRECTORY,
                WORKING_DIRECTORY
            )
            start_capture(
                session,
                sensor,
                comp_name,
                PARENT_DIRECTORY,
                WORKING_DIRECTORY,
                FILE_NAME
            )

            try:
                sleep(capture_time)
            except KeyboardInterrupt:
                print("Caught keyboard interrupt")
            print("Stopping packet capture now")

            end_capture(
                session,
                PARENT_DIRECTORY,
                WORKING_DIRECTORY,
                FILE_NAME
            )
            cleanup_and_return(
                session,
                sensor,
                comp_name,
                dir_exists,
                PARENT_DIRECTORY,
                WORKING_DIRECTORY,
                FILE_NAME
            )


def main():

    # Handle Commandline arguments
    parser = ArgumentParser(
        description='Capture packets from remote hosts using CbLR'
    )
    parser.add_argument(
        '--hostname',
        help='Provide a single hostname to capture',
        default=''
    )
    parser.add_argument(
        '--hosts',
        help='Provide filepath of hostnames',
        default='hostnames'
    )
    parser.add_argument(
        '--profile', '-p',
        help='Provide the name of the cbapi profile to use',
        default='default'
    )
    parser.add_argument(
        '--seconds', '-s',
        help='Provide time to run capture',
        default='60',
        type=int
    )
    args = parser.parse_args()

    capture_packets(args.hostname, args.hosts, args.profile, args.seconds)

if __name__ == '__main__':
    from sys import exit
    exit(main())
