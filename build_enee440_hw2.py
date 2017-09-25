from makeshells import gcc_builders
from foreman import blueprint, foreman

script_path = "./build_blinky.sh"
build_blinky = gcc_builders.ShellScript(script_path)

common_flags = "-mthumb-interwork -g -mcpu=cortex-m7 -mthumb "

build_flags = common_flags + "-c -gdwarf-2 -MD -Wall -O0 -mapcs-frame " \
              "-fdata-sections -ffunction-sections -std=gnu99 "

link_flags = common_flags + "-Wl,--gc-sections " \
              "-T resource/linkSTM32F767ZI-Nucleo.ld " \
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
binary_dir = "./binary/"

myincludes03_h = blueprint.Blueprint(
  name = source_dir + "myIncludes03.h",
  builder = collect,
  materials = [],
  foundation = []
)
myDataOps01_h = blueprint.Blueprint(
  name = source_dir + "myDataOps01.h",
  builder = collect,
  materials = [],
  foundation = []
)
mymain04_c = blueprint.Blueprint(
  name = source_dir + "mymain04.c",
  builder = collect,
  materials = [],
  foundation = []
)
startup_stm32f767xx_gcc_git01_S = blueprint.Blueprint(
  name = source_dir + "startup_stm32f767xx_gcc_git01.S",
  builder = collect,
  materials = [],
  foundation = []
)
mySystemInit_S = blueprint.Blueprint(
  name = source_dir + "mySystemInit.S",
  builder = collect,
  materials = [],
  foundation = []
)
myDataOps01_S = blueprint.Blueprint(
  name = source_dir + "myDataOps01.S",
  builder = collect,
  materials = [],
  foundation = []
)

startup_stm32f767xx_gcc_git01_o = blueprint.Blueprint(
  name = binary_dir + "startup_stm32f767xx_gcc_git01.o",
  builder = build,
  materials = [startup_stm32f767xx_gcc_git01_S],
  foundation = [startup_stm32f767xx_gcc_git01_S]
)
mySystemInit_o = blueprint.Blueprint(
  name = binary_dir + "mySystemInit.o",
  builder = build,
  materials = [mySystemInit_S],
  foundation = [mySystemInit_S]
)
myDataOps01_o = blueprint.Blueprint(
  name = binary_dir + "myDataOps01.o",
  builder = build,
  materials = [myDataOps01_S],
  foundation = [myDataOps01_S]
)
mymain04_o = blueprint.Blueprint(
  name = binary_dir + "mymain04.o",
  builder = build,
  materials = [mymain04_c],
  foundation = [mymain04_c, myDataOps01_h]
)

blinky_elf = blueprint.Blueprint(
  name = binary_dir + "blinky.elf",
  builder = link,
  materials = [mymain04_o, startup_stm32f767xx_gcc_git01_o, mySystemInit_o, 
               myDataOps01_o],
  foundation = [mymain04_o, startup_stm32f767xx_gcc_git01_o, mySystemInit_o, 
                myDataOps01_o]
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
