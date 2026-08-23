import os
import sys
import asyncio
import json
import random
import time
import binascii
import ssl
from datetime import datetime

import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# =================== IMPORTS FROM YOUR PROJECT ===================
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from protobuf_decoder.protobuf_decoder import Parser
    from Pb2 import MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
    from xC4 import CrEaTe_ProTo, GeneRaTePk, Ua, DecodE_HeX
except ImportError as e:
    print(f"⚠️ Warning: Some local modules missing: {e}")
    print("Please make sure you run this script in the same folder as your Pb2 and xC4 files.")

# =================== CONFIGURATION ===================
# 🔴 আপনার টেলিগ্রাম বটের টোকেন এখানে দিন (BotFather থেকে পাবেন) 🔴
TELEGRAM_TOKEN = "8743019008:AAEkYnqp6JErzZhaIBrHGvomIAOMXb3sNHc"

# 🔴 আপনার মেইন অ্যাকাউন্টের ইউআইডি এবং পাসওয়ার্ড এখানে দিন (যেটা দিয়ে স্ট্যাটাস চেক হবে) 🔴
MAIN_UID = "7036058426"
MAIN_PASS = "frexy_ARIYAN_AJVgdoWLnuyY"

REGION = "BD"

# =================== GLOBALS ===================
online_writer = None
whisper_writer = None
MAIN_KEY = None
MAIN_IV = None
status_response_cache = {}
active_spams = {}
bot_running = True

# =================== CRYPTO & HELPERS ===================
x_list = ['1','01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']

def Encrypt(number):
    number = int(number)
    encoded_bytes = []
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes).hex()

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def nmnmmmmn(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)

# =================== AUTH FUNCTIONS ===================
Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB54"
}

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = Hr.copy()
    headers["Host"] = "100067.connect.garena.com"
    headers["Connection"] = "close"
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200: return None, None
            data = await response.json()
            return data.get("open_id"), data.get("access_token")

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.126.7"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.access_token = access_token
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    headers = Hr.copy()
    headers['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def EnC_PacKeT(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    
    # Generate timestamp hex securely
    encrypted_timestamp = hex(timestamp)[2:]
    if len(encrypted_timestamp) % 2 != 0:
        encrypted_timestamp = '0' + encrypted_timestamp

    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    
    headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# =================== TCP & PROTO PARSING ===================
def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type in ["varint", "string", "bytes"]:
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[str(result.field)] = field_data
    return result_dict

def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_dict = parse_results(parsed_results)
        return json.dumps(parsed_results_dict)
    except Exception as e:
        return None

def get_player_status(packet_bytes):
    json_result = get_available_room(packet_bytes)
    if not json_result: return "OFFLINE"
    parsed_data = json.loads(json_result)
    
    try:
        status = parsed_data["5"]["data"]["1"]["data"]["3"]["data"]
        if status == 1: return "SOLO"
        if status == 2:
            group_count = parsed_data["5"]["data"]["1"]["data"].get("9", {}).get("data", 0)
            countmax1 = parsed_data["5"]["data"]["1"]["data"].get("10", {}).get("data", 0)
            return f"INSQUAD ({group_count}/{countmax1+1})"
        if status in [3, 5]: return "INGAME"
        if status == 4: return "IN_ROOM"
        if status in [6, 7]: return "IN SOCIAL ISLAND MODE"
    except:
        pass
    return "OFFLINE"

def get_idroom_by_idplayer(packet_bytes):
    try:
        json_result = get_available_room(packet_bytes)
        parsed_data = json.loads(json_result)
        return parsed_data["5"]["data"]["1"]["data"]['15']["data"]
    except:
        return None

async def createpacketinfo(idddd, key, iv):
    try:
        ida = Encrypt(idddd)
        packet = f"080112090A05{ida}1005"
        header_lenth = len(await encrypt_packet(packet, key, iv)) // 2
        header_lenth_final = dec_to_hex(header_lenth)
        
        final_packet = f"0F15{'0'*(9-len(header_lenth_final))}{header_lenth_final}" + await nmnmmmmn(packet, key, iv)
        return bytes.fromhex(final_packet)
    except Exception as e:
        print(f"Error creating packet info: {e}")
        return None

BADGE_VALUES = {"s1": 1048576, "s2": 32768, "s3": 2048, "s4": 64, "s5": 262144}

async def request_join_with_badge(target_uid, badge_value, key, iv, region="BD"):
    try:
        fields = {
            1: 33,
            2: {
                1: int(target_uid),
                2: region.upper(),
                3: 1,
                4: 1,
                5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                6: "iG:[C][B][FF0000] BOT",
                7: 330,
                8: 1000,
                10: region.upper(),
                11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56, 97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
                12: 1,
                13: int(target_uid),
                16: 1,
                17: 1,
                18: 312,
                19: 46,
                23: bytes([16, 1, 24, 1]),
                24: 902050001,
                31: {1: 1, 2: badge_value},
                32: badge_value,
                34: {1: int(target_uid), 2: 8, 3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])}
            },
            10: "en",
            13: {2: 1, 3: 1}
        }
        
        packet = (await CrEaTe_ProTo(fields)).hex()
        packet_type = '0519' if region.lower() == 'bd' else '0514'
        return await GeneRaTePk(packet, packet_type, key, iv)
    except Exception as e:
        print(f"Error request_join_with_badge: {e}")
        return None

# =================== BACKGROUND MAIN TASK ===================
async def maintain_connection():
    global online_writer, MAIN_KEY, MAIN_IV
    
    if MAIN_UID == "7036058426" or MAIN_PASS == "frexy_ARIYAN_AJVgdoWLnuyY":
        print("⚠️ Warning: Please configure MAIN_UID and MAIN_PASS in the code!")
        return
        
    while bot_running:
        try:
            print("Connecting MAIN account...")
            open_id, access_token = await GeNeRaTeAccEss(MAIN_UID, MAIN_PASS)
            if not open_id:
                print("Failed to get open_id for MAIN")
                await asyncio.sleep(5)
                continue
                
            PyL = await EncRypTMajoRLoGin(open_id, access_token)
            MajoRLoGinResPonsE = await MajorLogin(PyL)
            if not MajoRLoGinResPonsE:
                print("Failed MajorLogin")
                await asyncio.sleep(5)
                continue
                
            MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
            MAIN_KEY = MajoRLoGinauTh.key
            MAIN_IV = MajoRLoGinauTh.iv
            
            LoGinDaTa = await GetLoginData(MajoRLoGinauTh.url, PyL, MajoRLoGinauTh.token)
            LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
            
            OnLineiP, OnLineporT = LoGinDaTaUncRypTinG.Online_IP_Port.split(":")
            
            AutHToKen = await xAuThSTarTuP(int(MajoRLoGinauTh.account_uid), MajoRLoGinauTh.token, int(MajoRLoGinauTh.timestamp), MAIN_KEY, MAIN_IV)
            
            reader, writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
            online_writer = writer
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            print("✅ MAIN account connected successfully!")
            
            while bot_running:
                data = await reader.read(9999)
                if not data:
                    print("Connection lost.")
                    break
                data_hex = data.hex()
                
                if data_hex.startswith('0f00'):
                    try:
                        if '08' in data_hex:
                            proto_part = data_hex.split("08", 1)[1]
                            packet_bytes = bytes.fromhex(f"08{proto_part}")
                            parsed_data = get_available_room(packet_bytes)
                            if parsed_data:
                                parsed_json = json.loads(parsed_data)
                                if "2" in parsed_json and parsed_json["2"].get("data") == 15:
                                    player_id = parsed_json["5"]["data"]["1"]["data"]["1"]["data"]
                                    player_status = get_player_status(packet_bytes)
                                    room_id = get_idroom_by_idplayer(packet_bytes)
                                    
                                    status_response_cache[str(player_id)] = {
                                        'status': player_status,
                                        'room_id': room_id,
                                        'timestamp': time.time()
                                    }
                    except Exception as e:
                        print(f"Status parse error: {e}")
                        
            online_writer.close()
            await online_writer.wait_closed()
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)

# =================== TELEGRAM HANDLERS ===================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "╔══════════════════════════════════════════════════╗\n"
        "║                     FREXY BOT                   ║\n"
        "╠══════════════════════════════════════════════════╣\n"
        "║ 🔥 WELCOME TO FREXY BOT 🔥                      ║\n"
        "║                                                  ║\n"
        "║ 📌 Version: OB54 - 1.126.7                       ║\n"
        "║ BD & IND Dual Server Keep-Alive Active.          ║\n"
        "║                                                  ║\n"
        "║ 👉 /status <UID> – প্লেয়ার স্ট্যাটাস কুয়েরি করুন        ║\n"
        "║ 👉 /room <UID> [Minutes] – স্বয়ংক্রিয় দ্বৈত কুয়েরি + কাস্টম অটো স্প্যাম ║\n"
        "║ 👉 /stop <UID> – নির্দিষ্ট ইউজারের স্প্যাম বন্ধ করুন       ║\n"
        "║ 👉 /list – স্প্যাম তালিকা দেখুন                      ║\n"
        "╚══════════════════════════════════════════════════╝"
    )
    await update.message.reply_text(msg)

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ব্যবহার: /status <UID>")
        return
        
    uid = context.args[0]
    if not online_writer or not MAIN_KEY:
        await update.message.reply_text("বট এখনো সার্ভারে কানেক্ট হয়নি, অপেক্ষা করুন।")
        return
        
    status_packet = await createpacketinfo(uid, MAIN_KEY, MAIN_IV)
    if status_packet:
        online_writer.write(status_packet)
        await online_writer.drain()
        
        # Wait for response for up to 5 seconds
        for _ in range(15):
            await asyncio.sleep(0.5)
            if uid in status_response_cache:
                data = status_response_cache[uid]
                status = data['status']
                
                # Build reply
                reply = f"🟢 Server:\n{REGION}\n"
                reply += "╔══════════════════════════════════════════════════╗\n"
                reply += "║              🌟 WINTER FREXY PLAYER STATUS 🌟               ║\n"
                reply += "╠══════════════════════════════════════════════════╣\n"
                reply += f"  👤 Target UID      :: {uid}\n"
                reply += f"  📊 Garena State    :: {status}\n"
                
                if "IN_ROOM" in status:
                    reply += f"  📝 Description     :: কাস্টম রুমে আছেন (In Custom Room)\n"
                    reply += f"  🏠 Custom Room ID  :: {data.get('room_id', 'N/A')}\n"
                elif "INGAME" in status:
                    reply += f"  📝 Description     :: ম্যাচের ভেতরে খেলছেন (In Game/Playing)\n"
                elif "INSQUAD" in status:
                    reply += f"  📝 Description     :: গ্রুপে বা স্কোয়াডে আছেন (In Group/Squad)\n"
                elif "SOLO" in status:
                    reply += f"  📝 Description     :: লবিতে একা দাঁড়িয়ে আছেন (Solo in Lobby)\n"
                elif "OFFLINE" in status:
                    reply += f"  📝 Description     :: প্লেয়ার অফলাইনে আছেন (Offline)\n"
                    
                reply += "╠══════════════════════════════════════════════════╣\n"
                reply += "║                 👑 POWERED BY WINTER FREXY 👑               ║\n"
                reply += "╚══════════════════════════════════════════════════╝"
                
                await update.message.reply_text(reply)
                return
                
        await update.message.reply_text("কোনো রেসপন্স পাওয়া যায়নি। প্লেয়ারটি অফলাইন হতে পারে বা সার্ভার ব্যস্ত।")

async def spam_task_loop(target_uid, minutes):
    end_time = time.time() + (minutes * 60)
    
    # Read accounts
    accounts = []
    try:
        with open("room_join.txt", "r") as f:
            for line in f:
                if ":" in line:
                    u, p = line.strip().split(":", 1)
                    accounts.append((u, p))
    except Exception as e:
        print(f"Could not load room_join.txt: {e}")
        pass
        
    if not accounts:
        return
        
    badges = ["s1", "s2", "s3", "s4", "s5"]
    
    while time.time() < end_time and active_spams.get(target_uid):
        for acc_uid, acc_pass in accounts:
            if not active_spams.get(target_uid):
                break
                
            try:
                # Login specific bot
                open_id, access_token = await GeNeRaTeAccEss(acc_uid, acc_pass)
                if not open_id: continue
                PyL = await EncRypTMajoRLoGin(open_id, access_token)
                MajoRLoGinResPonsE = await MajorLogin(PyL)
                MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
                
                acc_key = MajoRLoGinauTh.key
                acc_iv = MajoRLoGinauTh.iv
                
                LoGinDaTa = await GetLoginData(MajoRLoGinauTh.url, PyL, MajoRLoGinauTh.token)
                LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
                
                OnLineiP, OnLineporT = LoGinDaTaUncRypTinG.Online_IP_Port.split(":")
                AutHToKen = await xAuThSTarTuP(int(MajoRLoGinauTh.account_uid), MajoRLoGinauTh.token, int(MajoRLoGinauTh.timestamp), acc_key, acc_iv)
                
                reader, writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
                writer.write(bytes.fromhex(AutHToKen))
                await writer.drain()
                await asyncio.sleep(1)
                
                badge_name = random.choice(badges)
                badge_val = BADGE_VALUES[badge_name]
                
                pkt = await request_join_with_badge(target_uid, badge_val, acc_key, acc_iv, REGION)
                if pkt:
                    writer.write(pkt)
                    await writer.drain()
                    
                await asyncio.sleep(0.5)
                writer.close()
                await writer.wait_closed()
                
            except Exception as e:
                print(f"Spam acc error: {e}")
                
            await asyncio.sleep(2)
            
    if target_uid in active_spams:
        del active_spams[target_uid]

async def room_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ব্যবহার: /room <UID> [Minutes]")
        return
        
    uid = context.args[0]
    minutes = int(context.args[1]) if len(context.args) > 1 else 5
    
    if uid in active_spams:
        await update.message.reply_text(f"{uid} এর জন্য স্প্যাম আগে থেকেই চলছে!")
        return
        
    active_spams[uid] = True
    asyncio.create_task(spam_task_loop(uid, minutes))
    
    await update.message.reply_text(f"✅ {uid} এর রুমে/গ্রুপে {minutes} মিনিটের জন্য স্প্যাম শুরু হয়েছে!\n(room_join.txt থেকে ইউজার লগিন করে রিকোয়েস্ট পাঠানো হচ্ছে)")

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ব্যবহার: /stop <UID>")
        return
    uid = context.args[0]
    if uid in active_spams:
        active_spams[uid] = False
        del active_spams[uid]
        await update.message.reply_text(f"🛑 {uid} এর স্প্যাম বন্ধ করা হয়েছে!")
    else:
        await update.message.reply_text("এই UID তে কোনো স্প্যাম চলছে না।")

async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not active_spams:
        await update.message.reply_text("কোনো স্প্যাম চলছে না।")
        return
    reply = "চলমান স্প্যাম তালিকা:\n"
    for uid in active_spams:
        reply += f"🔹 {uid}\n"
    await update.message.reply_text(reply)

def main():
    # Generate default room_join.txt if not exists
    if not os.path.exists("room_join.txt"):
        with open("room_join.txt", "w") as f:
            f.write("UID:PASS\n")
            
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ Error: Please put your Telegram Bot Token in TELEGRAM_TOKEN")
        return

    print("🚀 Starting Telegram Bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("room", room_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    
    # Start background TCP connection task
    loop = asyncio.get_event_loop()
    loop.create_task(maintain_connection())
    
    print("✅ Bot is running! Type /start in your Telegram bot.")
    app.run_polling()

if __name__ == "__main__":
    main()
