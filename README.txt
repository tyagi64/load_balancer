Load Balancing Project

This project explores two approaches to load balancing: using virtual machines and using microservices with Linux processes.

Directory Structure

- loadbs_vm: Virtual Machine Approach
    - setup.py: Script to create a virtual machine and set up the load balancing environment
    - master.py: Master node responsible for load balancing
    - slave.py: Slave node that handles incoming requests
- loadbs_microserv: Microservices Approach
    - master: Master node responsible for load balancing
        - master.py: Master node code
    - tester: Tester code to test the load balancer
        - tester.py: Tester code

Setup and Requirements

- No VM disk or installer ISO is included in this archive. QEMU is used for virtual machine setup.
- The given code works on Linux environment.
- Python is required for running the setup scripts and load balancing code.

Usage

1. loadbs_vm:
    - Run setup.py to create a virtual machine and set up the load balancing environment.
    - Configure master.py and slave.py as needed.
    - Run master.py on the host OS to start the load balancer.
2. loadbs_microserv:
    - Run master/master.py to start the master node.
    - Use tester/tester.py to test the load balancer.