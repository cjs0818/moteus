#!/usr/bin/python3 -B

# Copyright 2023 mjbots Robotic Systems, LLC.  info@mjbots.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import moteus
import time
import math


'''Demonstrates how to specify alternate registers to query, and how
to control the velocity and acceleration limits on a per-command basis
to create a continouous trajectory.'''

POS_CMD = 0.5

async def cmd_stream(s, cmd):
	results = ( await s.command(cmd.encode('utf-8'), allow_any_response=True) ).decode('utf-8')
	print(results)
	#await asyncio.sleep(0.02)

async def stop(s):
	cmd = 'd stop'
	await cmd_stream(s, cmd)

async def stop_n_hold(s):
	cmd = 'd stop'
	await cmd_stream(s, cmd)
	cmd = f'd pos nan 0.0 1.0'
	await cmd_stream(s, cmd)

	# equivalent to
	#cmd = 'd zero'

async def pos_control(s, pos, vel=0, max_torque="nan"):
	cmd = f'd pos {pos} {vel} {max_torque}'
	await cmd_stream(s, cmd)

async def main():
	qr = moteus.QueryResolution()
	qr._extra = {
		moteus.Register.CONTROL_POSITION : moteus.F32,
		moteus.Register.CONTROL_VELOCITY : moteus.F32,
		moteus.Register.CONTROL_TORQUE : moteus.F32,
		moteus.Register.POSITION_ERROR : moteus.F32,
		moteus.Register.VELOCITY_ERROR : moteus.F32,
		moteus.Register.TORQUE_ERROR : moteus.F32,
		}

	c = moteus.Controller(query_resolution = qr)
	s = moteus.Stream(c)

	# Clear any faults.
	await c.set_stop()  
	#------------
	# Equal to
	'''
		await s.command(
			b'd stop',
			allow_any_response=True)

			#Reference
			#old_kp = float((await s.command(
			#    b'conf get servo.pid_position.kp',
			#    allow_any_response=True)).decode('utf8'))
	'''
	#------------

	#cmd = f'conf set servo.pid_position.kp {new_kp}'
	#cmd = f'd  stop'
	#await s.command(cmd.encode('utf8'))

	'''
	#----------------
	# stop
	#	d stop
	#		->  cmd = 'd stop'
	#			results = (await s.command(cmd.encode('utf-8'), allow_any_response=True)).decode('utf-8')
	#			print(results)

	#----------------
	# control
	#position control
	# 	d pos 0.5 0 1   
	# 		->  cmd = f'd pos {pos} {vel} {max_torque}'
	#			results = (await s.command(cmd.encode('utf-8'), allow_any_response=True)).decode('utf-8')
	#			print(results)
	#volocity control
	#	d pos nan 1 1
	#	<options>
	
		p - kp scale: the configured kp value is multiplied by this constant for the duration of this command
		d - kd scale: the configured kd value is multiplied by this constant for the duration of this command
		s - stop position: when a non-zero velocity is given, motion stops when the control position reaches this value.
		f - feedforward torque in Nm
		t - timeout: If another command is not received in this many seconds, enter the timeout mode.
		v - velocity limit: the given value will override the global velocity limit for the duration of this command.
		a - acceleration limit: the given value will override the global acceleration limit for the duration of this command.
		o - fixed voltage override: while in affect, treat the control as if fixed_voltage_mode were enabled with the given voltage
	'''

	#----------------
	# ex. of stop
	cmd = 'd stop'
	await cmd_stream(s, cmd)

	# equivalent to
	#		stop(s)

	#----------------
	# exact 0 (set current position as 0)
	cmd = 'd exact 0'
	await cmd_stream(s, cmd)

	#----------------
	# ex. of position control
	#position = 0.5; velocity = 0; max_torque = 1
	#cmd = f'd pos {position} {velocity} {max_torque}'
	#results = (await s.command(cmd.encode('utf-8'), allow_any_response=True)).decode('utf-8')
	#print(results)

	#----------------
	# ex. of velocity control
	#position = math.nan; velocity = 1; max_torque = 1
	#cmd = f'd pos {position} {velocity} {max_torque}'
	#results = (await s.command(cmd.encode('utf-8'), allow_any_response=True)).decode('utf-8')
	#print(results)

	#-----------------
	# ex. of velocity control using set_position
	#	This is different from 'd pos' command in that motor has been stopped when Ctrl-C
	#state = await c.set_position(position=math.nan, velocity=5, query=True)
	#print(state)
	#


	#----------------
	# ex. of get parameters
	#cmd = b'conf get servo.pid_position.kp'
	#results = float( (await s.command(cmd, allow_any_response=True)).decode('utf-8') )
	#print(results)

	#----------------
	# ex. of set parameters
	#new_kp = 4.0; cmd = f'conf set servo.pid_position.kp {new_kp}'
	#results = (await s.command(cmd.encode('utf-8'), allow_any_response=True)).decode('utf-8')
	#print(results)

	#----------------
	# ex. of set parameters
	position_max = 1; cmd = f'conf set servopos.position_max {position_max}'
	await cmd_stream(s, cmd)

	position_min = -position_max; cmd = f'conf set servopos.position_min {position_min}'
	await cmd_stream(s, cmd)


	pos = 0.5; await pos_control(s, pos)
	#await pos_control(s, pos, vel, max_torque) #default: vel=0, max_torque = "nan" (system-wide configured maximum torque)


	#state = await c.set_position(position=math.nan, query=True)
	# Print out everything.
	#print(state)
	
	print("Just after cmd 'd pos'")

	#------------------------------------
	# Read Data
	name = 'motor_position'
		# Possible 'name's can be acquired by 'tel list' command
	
		#>>> tel list
		#	system_info
		#	firmware
		#	aux1
		#	ic_pz1
		#	aux2
		#	ic_pz2
		#	motor_position
		#	drv8323
		#	servo_stats
		#	servo_cmd
		#	servo_control
		#	board_debug
		#	git
	results = await s.read_data(name)
	print(results)
	#print(results.position)
	#------------------------------------

	while True:
		await asyncio.sleep(1)


	cmd = 1

	results = await c.set_position(
		position=cmd,
		velocity=0.0,
		maximum_torque = 1.0,
		#accel_limit=1.0,
		#velocity_limit=3.0,
		#feedforward_torque = 0.2,
		query=True,
	)

	print(results)

	print("\n Position before control:", results.values[moteus.Register.POSITION], "\n")
	await asyncio.sleep(1)

	#await stop_n_hold(s)

	while True:
		# Print out everything.
		#state = await c.set_position(position=math.nan, query=True)
		#print(f'{state}\n\n')
		await asyncio.sleep(1)
	




	'''
	while True:
		# Our command position will alternate between 0.5 and -0.5
		# every second.
		current_command = POS_CMD if (round(time.time()) % 2) else -POS_CMD

		#current_command = -POS_CMD

		# The acceleration and velocity limit could be configured as
		# `servo.default_accel_limit` and
		# `servo.default_velocity_limit`.  We will override those
		# configurations here on a per-command basis to ensure that
		# the limits are always used regardless of config.
		results = await c.set_position(
			position=current_command,
			velocity=0.0,
			#feedforward_torque = 0.2,
			accel_limit=8.0,
			velocity_limit=3.0,
			query=True,
		)

		# Velocity Control: position = math.nan

		print(results)

		print("Position:", results.values[moteus.Register.POSITION], "\n")

		await asyncio.sleep(0.02)
	'''

if __name__ == '__main__':
	asyncio.run(main())

