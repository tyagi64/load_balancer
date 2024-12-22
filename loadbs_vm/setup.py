import sys 
import os


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file = open(sys.argv[1]).readlines()
        config_file = [ i.replace('\n','') for i in config_file]
        hostname = config_file[0]
        num_sys = int(config_file[1])
        for i in range(0,num_sys):
                os.system(f"qemu-img create -f qcow2 slave_{config_file[i+3]} 10G")
                os.system(f"qemu-system-x86_64 -no-reboot  -m 2048 \
  -cdrom <path to iso> \
  -drive if=virtio,file=<path to disk>,format=qcow2 \
  -enable-kvm \
  -netdev user,id=mynet0,hostfwd=tcp:127.0.0.1:7922-:22\
  -device virtio-net,netdev=mynet0 \
  -smp 2 \{config_file[i+3]}")
        input("Enter if done")
        for i in range(0,num_sys):
            os.system(f"scp -P {config_file[i+3]} slave.py root@localhost:/root/")
            input("Continue...")
    else:
        print("Provide the configuration file")
