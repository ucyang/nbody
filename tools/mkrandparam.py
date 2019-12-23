#!/usr/bin/env python3
# Make random parameters for N-body GUI simulator.

import sys
import random

# Check parameters.
if len(sys.argv) < 16:
    print("Please specify arguments correctly.")
    print("Usage: mkrandparam.py <count> <m_min> <m_max> " +
          "<x_min> <y_min> <z_min> <x_max> <y_max> <z_max> " +
          "<vx_min> <vy_min> <vz_min> <vx_max> <vy_max> <vz_max>")
    sys.exit(0x1)

count = int(sys.argv[1])

m_min = float(sys.argv[2])
m_max = float(sys.argv[3])

x_min = float(sys.argv[4])
y_min = float(sys.argv[5])
z_min = float(sys.argv[6])

x_max = float(sys.argv[7])
y_max = float(sys.argv[8])
z_max = float(sys.argv[9])

vx_min = float(sys.argv[10])
vy_min = float(sys.argv[11])
vz_min = float(sys.argv[12])

vx_max = float(sys.argv[13])
vy_max = float(sys.argv[14])
vz_max = float(sys.argv[15])

print(count)

for i in range(count):
    print(random.uniform(m_min, m_max),
          random.uniform(x_min, x_max),
          random.uniform(y_min, y_max),
          random.uniform(z_min, z_max),
          random.uniform(vx_min, vx_max),
          random.uniform(vy_min, vy_max),
          random.uniform(vz_min, vz_max))
