import requests
import base64

# amonet => 360p
# rtveplayw => 720p?

def bytearrayToInt(data):
    t0 = data[0]
    t1 = data[1]
    t2 = data[2]
    t3 = data[3]
    return t0 << 24 | t1 << 16 | t2 << 8 | t3

def readPngChunk(data, pointer):
    data_length = bytearrayToInt(data[pointer:pointer+4])
    pointer += 4

    type = data[pointer:pointer+4].decode()
    pointer += 4
    
    extracted_data = b''
    for i in range(data_length):
        extracted_data = extracted_data + data[pointer:pointer+1]
        pointer += 1
    pointer += 4
    return (type, extracted_data, pointer)


def processPart1(p1):
    first_p2 = b''
    cnt1 = 0
    cnt2 = 0
    for i in range(len(p1)):
        if cnt1 == 0:
            first_p2 = first_p2 + p1[i:i+1]
            cnt2 = (cnt2 + 1)%4
            cnt1 = cnt2
        else:
            cnt1 -= 1
    return first_p2

def processTextSegment(text_raw):
    #print("ProcessText_")

    text = text_raw.replace(b'\x00', b'')
    portions = text.split(b'#')
    #print(portions)

    first = portions[0]

    #print(first)

    first_p2 = processPart1(first)
    #print(first_p2)
    
    #print(text)
    if b'%%' in text:
        print("aaa")
    split2 = portions[1].split(b'%%')

    second = portions[1]
    final = b''

    n = 0
    s = 3
    h = 0

    for i in range(len(second)):
        if n == 0:
            a = int(second[i:i+1]) * 10
            n = 1
            
        else:
            if s == 0:
                a += int(second[i:i+1])
                final = final + first_p2[a:a+1]
                s = (h) % 4
                n = 0
                h += 1
            else:
                s -= 1
    
    return final


#type, data, pointer = readPngChunk(bytearray,pointer)

def get_urls(video_id):
    #b64 = requests.get("http://ztnr.rtve.es/ztnr/movil/thumbnail/banebdyede/videos/6948300.png?q=v2").text
    b64 = requests.get(f"http://ztnr.rtve.es/ztnr/movil/thumbnail/rtveplayw/videos/{video_id}.png?q=v2").text
    #print(b64)
    bytearray = base64.b64decode(b64)


    type = None
    pointer = 8
    data = None

    urls = []

    while True:
        if "IEND" == type:
            break
        type, data, pointer = readPngChunk(bytearray,pointer)
        
        if type == "tEXt":
            urls.append(processTextSegment(data))
    
    #print(urls)
    return urls

    #print(type,data,pointer)
    

#get_urls(6948300)