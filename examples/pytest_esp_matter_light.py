# SPDX-License-Identifier: CC0-1.0

import pathlib
import pytest
import time
import re
import pexpect
import subprocess
import netifaces
from typing import Tuple
from pytest_embedded import Dut
import threading

CURRENT_DIR_LIGHT = str(pathlib.Path(__file__).parent)+'/light'
CHIP_TOOL_EXE = str(pathlib.Path(__file__).parent)+ '/../connectedhomeip/connectedhomeip/out/host/chip-tool'
OT_BR_EXAMPLE_PATH = str(pathlib.Path(__file__).parent)+'/../esp-thread-br/examples/basic_thread_border_router'
pytest_build_dir = CURRENT_DIR_LIGHT
pytest_matter_thread_dir = CURRENT_DIR_LIGHT+'|'+OT_BR_EXAMPLE_PATH


@pytest.mark.esp32c2
@pytest.mark.esp32c3
@pytest.mark.esp32c6
@pytest.mark.esp_matter_dut
@pytest.mark.parametrize(
    ' count, app_path, target, erase_all', [
        ( 4, pytest_build_dir, 'esp32|esp32c2|esp32c3|esp32c6', 'y|y|y|y'),
    ],
    indirect=True,
)
def run_the_heap_dump_test(dut: Dut) -> None:
    light = dut
    light.expect(r'chip\[DL\]\: Configuring CHIPoBLE advertising', timeout=20)
    time.sleep(5)

    # List to store heap dump data
    heap_dumps = []

    # Lock for thread-safe list operations
    heap_dumps_lock = threading.Lock()

    # Function to monitor device logs
    def monitor_logs():
        while True:
            try:
                line = light.read_line(timeout=1)
                if "========== HEAP-DUMP-START ==========" in line:
                    heap_dump = []
                    while True:
                        heap_line = light.read_line(timeout=1)
                        if "========== HEAP-DUMP-END ==========" in heap_line:
                            break
                        heap_dump.append(heap_line)
                    with heap_dumps_lock:
                        heap_dumps.append("".join(heap_dump))
            except pexpect.TIMEOUT:
                continue
            except pexpect.EOF:
                break

    # Start log monitoring in a separate thread
    log_thread = threading.Thread(target=monitor_logs, daemon=True)
    log_thread.start()

    # Run commissioning
    command = CHIP_TOOL_EXE + ' pairing ble-wifi 1 ChipTEH2 chiptest123 20202021 3840'
    out_str = subprocess.getoutput(command)
    print(out_str)

    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
        assert False

    # Wait for a short time to allow log processing
    time.sleep(5)

    # Ensure the log monitoring thread is terminated
    log_thread.join(timeout=1)

    # Process and analyze heap dumps
    for i, dump in enumerate(heap_dumps):
        print(f"Heap Dump {i + 1}:")
        print(dump)
        # Add your heap size analysis here

    #dump the heap stats
    print(heap_dumps)


@pytest.mark.esp32c3
@pytest.mark.esp_matter_dut
@pytest.mark.parametrize(
    ' count, app_path, target, erase_all', [
        ( 1, pytest_build_dir, 'esp32c3', 'y'),
    ],
    indirect=True,
)

# Matter over wifi commissioning
def test_matter_commissioning_c3(dut:Dut) -> None:
    light = dut
    # BLE start advertising
    light.expect(r'chip\[DL\]\: Configuring CHIPoBLE advertising', timeout=20)
    # Start commissioning
    time.sleep(5)
    command = CHIP_TOOL_EXE + ' pairing ble-wifi 1 ChipTEH2 chiptest123 20202021 3840'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-off the light
    time.sleep(3)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-on the light
    time.sleep(5)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False

@pytest.mark.esp32c2
@pytest.mark.esp_matter_dut
@pytest.mark.parametrize(
    ' count, app_path, target, erase_all', [
        ( 1, pytest_build_dir, 'esp32c2', 'y'),
    ],
    indirect=True,
)

# Matter over wifi commissioning
def test_matter_commissioning_c2(dut:Dut) -> None:
    light = dut
    # BLE start advertising
    light.expect(r'chip\[DL\]\: Configuring CHIPoBLE advertising', timeout=20)
    # Start commissioning
    time.sleep(5)
    command = CHIP_TOOL_EXE + ' pairing ble-wifi 1 ChipTEH2 chiptest123 20202021 3840'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-off the light
    time.sleep(3)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-on the light
    time.sleep(5)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False

@pytest.mark.esp32c6
@pytest.mark.esp_matter_dut
@pytest.mark.parametrize(
    ' count, app_path, target, erase_all', [
        ( 1, pytest_build_dir, 'esp32c6', 'y'),
    ],
    indirect=True,
)

# Matter over wifi commissioning
def test_matter_commissioning_c6(dut:Dut) -> None:
    light = dut
    # BLE start advertising
    light.expect(r'chip\[DL\]\: Configuring CHIPoBLE advertising', timeout=20)
    # Start commissioning
    time.sleep(5)
    command = CHIP_TOOL_EXE + ' pairing ble-wifi 1 ChipTEH2 chiptest123 20202021 3840'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-off the light
    time.sleep(3)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-on the light
    time.sleep(5)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False


# get the host interface name
def get_host_interface_name() -> str:
    interfaces = netifaces.interfaces()
    interface_name = [s for s in interfaces if 'wl' in s][0]
    return str(interface_name)


# reset host interface
def reset_host_interface() -> None:
    interface_name = get_host_interface_name()
    flag = False
    try:
        command = 'ifconfig ' + interface_name + ' down'
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(1)
        command = 'ifconfig ' + interface_name + ' up'
        subprocess.call(command, shell=True, timeout=10)
        time.sleep(1)
        flag = True
    finally:
        time.sleep(1)
        assert flag


# set interface sysctl options
def set_interface_sysctl_options() -> None:
    interface_name = get_host_interface_name()
    flag = False
    try:
        command = 'sysctl -w net/ipv6/conf/' + interface_name + '/accept_ra=2'
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(1)
        command = 'sysctl -w net/ipv6/conf/' + interface_name + '/accept_ra_rt_info_max_plen=128'
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(1)
        command = 'sysctl -w net.ipv6.conf.all.forwarding=1'
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(1)
        flag = True
    finally:
        time.sleep(2)
        assert flag


# initialize interface ipv6 address
def init_interface_ipv6_address() -> None:
    interface_name = get_host_interface_name()
    flag = False
    try:
        command = 'ip -6 route | grep ' + interface_name + " | grep ra | awk {'print $1'} | xargs -I {} ip -6 route del {}"
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(0.5)
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(1)
        command = 'ip -6 address show dev ' + interface_name + \
            " scope global | grep 'inet6' | awk {'print $2'} | xargs -I {} ip -6 addr del {} dev " + interface_name
        subprocess.call(command, shell=True, timeout=5)
        time.sleep(1)
        flag = True
    finally:
        time.sleep(1)
        assert flag


def fixture_Init_interface() -> bool:
    print('Init interface')
    init_interface_ipv6_address()
    reset_host_interface()
    time.sleep(30)
    set_interface_sysctl_options()
    return True


@pytest.mark.esp32h2
@pytest.mark.esp32s3
@pytest.mark.esp_matter_dut
@pytest.mark.parametrize(
    'count, app_path, target, erase_all', [
        ( 2, pytest_matter_thread_dir, 'esp32h2|esp32s3', 'y|n'),
    ],
    indirect=True,
)

# Matter over thread commissioning
def test_matter_commissioning_h2(dut:Tuple[Dut, Dut]) -> None:
    ot_br = dut[1]
    light = dut[0]
    # For matter over thread commissioning need to reset host interface
    fixture_Init_interface()
    # BLE start advertising
    light.expect(r'chip\[DL\]\: Configuring CHIPoBLE advertising', timeout=20)
    # flash ot_br
    ot_br.expect('OpenThread attached to netif', timeout=30)
    time.sleep(2)
    ot_br.write('factoryreset')
    ot_br.expect('OpenThread attached to netif', timeout=30)
    time.sleep(2)
    ot_br.write('log level 3')
    ot_br.expect('Done', timeout=5)
    time.sleep(2)
    # wifi connect -s ChipTEH2 -p chiptest123
    ot_br.write('wifi connect -s ChipTEH2 -p chiptest123')
    ot_br.expect('wifi sta is connected successfully', timeout=5)
    time.sleep(2)
    # start an ot network
    ot_br.write('ifconfig up')
    ot_br.expect('netif up', timeout=5)
    time.sleep(2)
    ot_br.write('thread start')
    ot_br.expect('Role detached -> leader', timeout=20)
    time.sleep(2)
   # get dataset
    ot_br.write('dataset active -x')
    dataset=ot_br.expect(r'\n(\w{202}\r)', timeout=5)[1].decode()
    print(dataset)
    ot_br.expect('ot_ext_cli: Got IPv6 event: Interface "sta" address: fdde:ad00:beef:cafe', timeout=30)
    print("Got unique local ipv6 address")
    # Start commissioning
    time.sleep(2)
    command = CHIP_TOOL_EXE + " pairing ble-thread 1 hex:{} ".format(dataset.strip())+"20202021 3840"
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-off the light
    time.sleep(2)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
    # Use toggle command to turn-on the light
    time.sleep(2)
    command = CHIP_TOOL_EXE + ' onoff toggle 1 1'
    out_str = subprocess.getoutput(command)
    print(out_str)
    result = re.findall(r'Run command failure', str(out_str))
    if len(result) != 0:
      assert False
