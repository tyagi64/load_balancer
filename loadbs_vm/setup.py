import sys 
import os


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file = open(sys.argv[1]).readlines()
        config_file = [ i.replace('\n','') for i in config_file]
        hostname = config_file[0]
        num_sys = int(config_file[1])
        os.system(f"qemu-img create -f qcow2 slave_{config_file[3]} 10G")
        os.system(f"qemu-system-x86_64 -no-reboot  -m 1024 -drive if=virtio,file=install74.img,format=raw  -drive if=virtio,file=slave_{config_file[3]},format=qcow2 -enable-kvm -netdev user,id=mynet0,hostfwd=tcp:0.0.0.0:{config_file[3]+20}-:22 -device virtio-net,netdev=mynet0-smp 1")
        input("Enter if done")
        os.system(f"scp -P {config_file[3]+20} slave.py root@localhost:/root/")
        input("poweroff the vm and press enter")
        for i in range(1,num_sys):
            os.system(f"cp slave_{config_file[3]} slave_{config_file[i+3]}")
    else:
        print("Provide the configuration file")
