import asyncio
import json
import psycopg2
import websockets
from datetime import datetime

#connect to database 
conn_db = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="yaroslav",
    host="localhost",
    port="5433"
)

#object for working with db
cur = conn_db.cursor()

#get latest row
cur.execute('SELECT MAX("time") FROM android_info')
row = cur.fetchone()
max_time = row[0] if row and row[0] is not None else 0

last = "{}"
flag = asyncio.Event()

#android server logic work
async def android(reader, writer):
	global last
	global max_time
 
	buffer = b""
 
	while True:
		data = await reader.read(4096)
  
		print(data)

		buffer += data
  
		while b"|||" in buffer:
			line, buffer = buffer.split(b"|||", 1)
   
			if not line:
				continue

			obj = json.loads(line.decode())
		
			if obj['time'] <= max_time:
				continue 
			
			max_time = obj['time']
			
			date = datetime.fromtimestamp(obj['time'] / 1000)
		
			cur.execute(
				'''
				INSERT INTO android_info (
					latitude, longitude, altitude,
					accuracy, speed, net_type, signal_lvl,
					band, earfcn, mcc, mnc, pci, tac, bandwidth,
					operator, rssi, rssnr, rsrp, rsrq, asu_level,
					cqi, timing_advance, bsic, arfcn, lac, mcc_gsm,
					psc, dbm, rssi_gsm, timing_advance_gsm, ber,
					asu_level_gsm, mnc_gsm, ddate, time
				) VALUES (
					%s, %s, %s, %s, %s, %s, %s,
					%s, %s, %s, %s, %s, %s, %s,
					%s, %s, %s, %s, %s, %s,
					%s, %s, %s, %s, %s, %s,
					%s, %s, %s, %s, %s, %s, %s, %s, %s
				)
				''',
				(
					obj["latitude"], obj["longitude"], obj["altitude"],
					obj["accuracy"], obj["speed"], obj["net_type"],
					obj["signal_lvl"], obj["band"], obj["earfcn"],
					obj["mcc"], obj["mnc"], obj["pci"], obj["tac"],
					obj["bandwidth"], obj["operator"], obj["rssi"],
					obj["rssnr"], obj["rsrp"], obj["rsrq"], obj["asu_level"],
					obj["cqi"], obj["timing_advance"], obj["bsic"],
					obj["arfcn"], obj["lac"], obj["mcc_gsm"], obj["psc"],
					obj["dbm"], obj["rssi_gsm"], obj["timing_advance_gsm"],
					obj["ber"], obj["asu_level_gsm"], obj["mnc_gsm"], date, obj['time']
				)
			)
			conn_db.commit()

			last = json.dumps(obj)
			print("Server receive from android: ", last)

			#signal to websocket (up flag)
			flag.set()

#send data to web
async def send_to_websocket(ws):
    while True:
        #wait flag
        await flag.wait()
        await ws.send(last)
        #down flag
        flag.clear()

async def main():
    print("Start server!")
    await asyncio.start_server(android, "0.0.0.0", 3500)
    await websockets.serve(send_to_websocket, "0.0.0.0", 3600)
    
    await asyncio.Future()

asyncio.run(main())
