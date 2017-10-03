from makeshells import gcc_builders
from foreman import blueprint, foreman

script_path = "./build_blinky.sh"
build_blinky = gcc_builders.ShellScript(script_path)

common_flags = "-mthumb-interwork -g -mcpu=cortex-m7 -mthumb "

build_flags = common_flags + "-c -gdwarf-2 -MD -Wall -O0 -mapcs-frame " \
              "-fdata-sections -ffunction-sections -std=gnu99 "

link_flags = common_flags + "-Wl,--gc-sections " \
              "-T resource/stm32f767zi.ld " \
              "-mcpu=cortex-m7 -mthumb -mthumb-interwork " \
              "-nostartfiles -nodefaultlibs -nostdlib  -lm "

collect = gcc_builders.hire_file_collector(build_blinky)
build = gcc_builders.hire_builder("arm-none-eabi-gcc", build_flags, build_blinky)
link = gcc_builders.hire_builder("arm-none-eabi-gcc", link_flags, build_blinky)
copy = gcc_builders.hire_objcopy("arm-none-eabi-objcopy", "-O ihex",
                                  build_blinky)
dump = gcc_builders.hire_objdump("arm-none-eabi-objdump", "-S", build_blinky)

wait = gcc_builders.hire_level_builder(build_blinky)

resource_dir = "./resource/"
source_dir = "./source/"
header_dir = "./header/"
binary_dir = "./binary/"

button_blink_h = blueprint.Blueprint(
  name = header_dir + "button_blink.h",
  builder = collect,
  materials = [],
  foundation = []
)
stm32f767xx_h = blueprint.Blueprint(
  name = header_dir + "stm32f767xx.h",
  builder = collect,
  materials = [],
  foundation = []
)
main_c = blueprint.Blueprint(
  name = source_dir + "main.c",
  builder = collect,
  materials = [],
  foundation = []
)
led_driver_S = blueprint.Blueprint(
  name = source_dir + "led_driver.S",
  builder = collect,
  materials = [],
  foundation = []
)
button_driver_S = blueprint.Blueprint(
  name = source_dir + "button_driver.S",
  builder = collect,
  materials = [],
  foundation = []
)
momentary_on_S = blueprint.Blueprint(
  name = source_dir + "momentary_on.S",
  builder = collect,
  materials = [],
  foundation = []
)
push_on_push_off_S = blueprint.Blueprint(
  name = source_dir + "push_on_push_off.S",
  builder = collect,
  materials = [],
  foundation = []
)
push_count_S = blueprint.Blueprint(
  name = source_dir + "push_count.S",
  builder = collect,
  materials = [],
  foundation = []
)
stm32f767xx_boot_S = blueprint.Blueprint(
  name = resource_dir + "stm32f767xx_boot.S",
  builder = collect,
  materials = [],
  foundation = []
)
stm32f767xx_reset_S = blueprint.Blueprint(
  name = resource_dir + "stm32f767xx_reset.S",
  builder = collect,
  materials = [],
  foundation = []
)

stm32f767xx_boot_o = blueprint.Blueprint(
  name = binary_dir + "stm32f767xx_boot.o",
  builder = build,
  materials = [stm32f767xx_boot_S],
  foundation = [stm32f767xx_boot_S]
)
stm32f767xx_reset_o = blueprint.Blueprint(
  name = binary_dir + "stm32f767xx_reset.o",
  builder = build,
  materials = [stm32f767xx_reset_S],
  foundation = [stm32f767xx_reset_S]
)
led_driver_o = blueprint.Blueprint(
  name = binary_dir + "led_driver.o",
  builder = build,
  materials = [led_driver_S],
  foundation = [led_driver_S]
)
button_driver_o = blueprint.Blueprint(
  name = binary_dir + "button_driver.o",
  builder = build,
  materials = [button_driver_S],
  foundation = [button_driver_S]
)
momentary_on_o = blueprint.Blueprint(
  name = binary_dir + "momentary_on.o",
  builder = build,
  materials = [momentary_on_S],
  foundation = [momentary_on_S]
)
push_on_push_off_o = blueprint.Blueprint(
  name = binary_dir + "push_on_push_off.o",
  builder = build,
  materials = [push_on_push_off_S],
  foundation = [push_on_push_off_S]
)
push_count_o = blueprint.Blueprint(
  name = binary_dir + "push_count.o",
  builder = build,
  materials = [push_count_S],
  foundation = [push_count_S]
)
main_o = blueprint.Blueprint(
  name = binary_dir + "main.o",
  builder = build,
  materials = [main_c],
  foundation = [main_c, button_blink_h]
)

blinky_elf = blueprint.Blueprint(
  name = binary_dir + "blinky.elf",
  builder = link,
  materials = [main_o, momentary_on_o, push_on_push_off_o, push_count_o,
               led_driver_o, button_driver_o, stm32f767xx_boot_o, 
               stm32f767xx_reset_o],
  foundation = [main_o, momentary_on_o, push_on_push_off_o, push_count_o,
               led_driver_o, button_driver_o, stm32f767xx_boot_o, 
               stm32f767xx_reset_o]
)

blinky_hex = blueprint.Blueprint(
  name = binary_dir + "blinky.hex",
  builder = copy,
  materials = [blinky_elf],
  foundation = [blinky_elf]
)
blinky_lst = blueprint.Blueprint(
  name = binary_dir + "blinky.lst",
  builder = dump,
  materials = [],
  foundation = []
)

foreman.bf_construct(blinky_hex, wait)
print("Generated: {}".format(script_path))
