# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, re, string, os, ast, pytz, urllib

botStart = time.time()
conf_dir = "./configs/"
cert_dir = "./certs/"

def LineClient(Email, Password):
    Client = LINE(idOrAuthToken=Email, passwd=Password, certificate=cert_dir+Email+".crt")
    return Client

cl = LineClient("kamibotver1@gmail.com","kamiv1")
kicker01 = LineClient("shengye9203181@gmail.com","rose920318")
kicker02 = LineClient("shengye9203182@gmail.com","rose920318")
kicker03 = LineClient("aa17699487@gmail.com","rose920318")

cl.log("Auth Token : " + str(cl.authToken))
oepoll = OEPoll(cl)
readOpen = codecs.open(conf_dir+"read.json","r","utf-8")
settingsOpen = codecs.open(conf_dir+"temp.json","r","utf-8")
read = json.load(readOpen)
settings = json.load(settingsOpen)

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

lineSettings = cl.getSettings()
kicker01Settings = kicker01.getSettings()
kicker02Settings = kicker02.getSettings()
kicker03Settings = kicker03.getSettings()

clProfile = cl.getProfile()
kicker01Profile = kicker01.getProfile()
kicker02Profile = kicker02.getProfile()
kicker03Profile = kicker03.getProfile()

clMID = cl.profile.mid
kicker01MID = kicker01.profile.mid
kicker02MID = kicker02.profile.mid
kicker03MID = kicker03.profile.mid

myProfile["displayName"] = clProfile.displayName
myProfile["statusMessage"] = clProfile.statusMessage
myProfile["pictureStatus"] = clProfile.pictureStatus

BG="uf87672295eeef310c67d5ce81bbf189d"
NC="u8adfb790a54a5f81ac2741cc2ede7ce7"
KAC=[kicker01,kicker02,kicker03]
owner=[BG, NC]
admin=[BG, NC, clMID, kicker01MID, kicker02MID, kicker03MID]
admin5=[BG, NC, clMID]
admin4=[BG, NC, clMID]
bots={clMID:cl, kicker01MID:kicker01, kicker02MID:kicker02, kicker03MID:kicker03}

msg_dict = {}
bl = [""]

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

def restartBot():
    print ("[Setting]Bot restart")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def backupData():
    try:
        backup = settings
        f = codecs.open(conf_dir+'temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open(conf_dir+'read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def logError(text):
    cl.log("[error] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))

def sendMessageWithMention(to, mid):
    try:
        data = '{"S":"0","E":"9","M":'+json.dumps(mid)+'}'
        text_ = '@MaFuTag '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+data+']}'}, contentType=0)
    except Exception as error:
        logError(error)

def helpmessage():
    helpMessage = """★BGBOT★
——☆MAFU專用☆——
【ad:@】增加權限者☆
【ra:@】刪除權限者☆
【mad:】使用mid增加權限☆
【mra:】使用mid刪除權限☆
——★系統指令★——
【bg:help】查看所有指令
【Update】重啟機器
【Uptime】運行時間
【@bg3sp】測試網速
——★機器設定★——
【Set】查看設定
【About】查看自己的狀態 
【Add On/Off】自動加入好友開關
【Join On/Off】自動入群開關
【Leave On/Off】自動離開副本開關
【Read On/Off】自動已讀開關
【Reread On/Off】顯示收回開關
【Qr On/Off】群組網址保護開關
【Qrjoin On/Off】網址自動入群開關
【Inviteprotect On/Off】群組邀請保護開關
——★一般指令★——
【Me】丟出自己友資
【Mid】查看自己Mid
【Name】查看名字
【Bio】查看個簽
【Picture】查看自己頭貼
【Cover】查看自己封面
【Contact @】查看標注者友資
【Mid @】查看標注者MID
【Name @】查看標注者名稱
【Bio @】查看標注者個簽
【Picture @ 】查看標注者頭貼
【Cover @ 】查看標注者封面
【Time】查看現在時間
【Gcreator】查看群主
【Gurl】丟出群組網址
【urlon】打開網址邀請
【urloff】關閉群組網址
【Glist】查看所有群組
【Gml】查看群組成員
【Ginfo】查看群組訊息
——★群組指令★——
【Ri @】重新邀請
【Tk @】多標注踢出
【Mk @ 】單獨標注踢出
【Vk @】清除訊息
【Vk: mid】清除訊息
【Nk】名稱踢出
【Uk  mid】踢出
【NT】名字標註成員
【Zk】踢出零字
【Zt】標註零字
【Zm】零字mid
【Cancel】取消所有成員邀請
【Gn】更改群組名稱
【Gc @】查看個資
【Inv  mid】邀請
【Ban @】黑單
【Unban @】解除黑單
【/cb】清空黑單
【Kill Ban】踢出黑單
【Tagall】標註全體
【Read on/off/reset】查看已讀開關
【Read】查看已讀
☆為MAFU專用指令
★Make by Mafu★"""
    return helpMessage

def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(op.param2)
            if settings["autoAdd"] == True:
                cl.sendMessage(op.param1, "hello {} Thx for add".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            print ("[11]有人打開群組網址 群組名稱: " + str(group.name) + "\n" + op.param1 + "\n名字: " + contact.displayName)
            if settings["qrprotect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if settings["inviteprotect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, [op.param3])
            if settings["autoJoin"] == True:
                if op.param2 in admin:
                    print ("進入群組: " + str(group.name))
                    cl.acceptGroupInvitation(op.param1)
                    G = cl.getGroup(op.param1)
                    if G.preventedJoinByTicket == True:
                        G.preventedJoinByTicket = False
                        cl.updateGroup(G)
                    Ti = cl.reissueGroupTicket(op.param1)
                    kicker01.acceptGroupInvitationByTicket(op.param1, Ti)
                    kicker02.acceptGroupInvitationByTicket(op.param1, Ti)
                    kicker03.acceptGroupInvitationByTicket(op.param1, Ti)
                    G.preventedJoinByTicket = True
                    cl.updateGroup(G)
                pass
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) + "\n" + op.param1 +"\n踢人者: " + contact1.displayName + "\nMid: " + contact1.mid + "\n被踢者" + contact2.displayName + "\nMid:" + contact2.mid )
            if settings["protect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
            elif op.param3 in owner:
                if op.param2 in admin:
                     pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.findAndAddContactsByMid(op.param3)
                    cl.inviteIntoGroup(op.param1,[op.param3])
            elif op.param3 in bots:
                if op.param2 in admin:
                    pass
                else:
                    bots_list = list(bots)
                    bots_list.remove(op.param3)
                    select = random.sample(bots_list, 1)
                    client = bots[select]
                    try:
                        print ("[19]有人踢機器 \n群組名稱: " + str(group.name) +"\n踢人者: " + contact.displayName + "\nMid: " + contact.mid + "\n\n")
                        client.kickoutFromGroup(op.param1,[op.param2])
                    except:    
                        bots_list.remove(select)
                        select = random.sample(bots_list, 1)
                        client = bots[select]
                        try:
                            client.kickoutFromGroup(op.param1,[op.param2])
                        except:
                            print ("機器踢人規制或是不在群組、\n["+op.param1+"]\nの\n["+op.param2+"]\n我踢不了他。\n把他加進黑名單。")
                    if op.param2 in settings["blacklist"]:
                        pass
                    else:
                        settings["blacklist"][op.param2] = True
                    G = client.getGroup(op.param1)
                    if G.preventedJoinByTicket == True:
                        G.preventedJoinByTicket = False
                        client.updateGroup(G)
                    Ti = client.reissueGroupTicket(op.param1)
                    bots[op.param3].acceptGroupInvitationByTicket(op.param1, Ti)
                    G.preventedJoinByTicket = True
                    client.updateGroup(G)
        if op.type == 24:
            print ("[ 24 ] 離開副本")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 1:
            print ("[1]")
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 13:
                if settings["contact"] == True:
                    msg.contentType = 0
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                            cl.sendMessage(msg.to,"[名稱]:\n" + msg.contentMetadata["名稱"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[個簽]:\n" + contact.statusMessage + "\n[頭像]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[名稱]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[個簽]:\n" + contact.statusMessage + "\n[頭像]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面]:\n" + str(cu))
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    msg.contentType = 0
                    msg.text = "Post URL\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendMessage(msg.to,msg.text)
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in admin:
                if text.lower() == 'bg:help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                if text.lower() == 'creator':
                	cl.sendContact(to, BG)
                if text.lower() == 'bomb':
                	cl.sendContact(to, "ua7fb5762d5066629323d113e1266e8ca")
                elif text.lower() == 'read on':
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%Y') + " - " + bln + " - " + timeNow.strftime('%d') + "\n" + timeNow.strftime('%H:%M:%S')
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open(conf_dir+'read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                cl.sendMessage(msg.to,"已設立已讀點")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open(conf_dir+'read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "設立已讀點:\n" + readTime)
                elif "Ban:" in msg.text:
                    midd = msg.text.replace("Ban:","")
                    try:
                        black["blacklist"][midd] = True
                        backupData()
                        cl.sendMessage(to, "已加入黑名單")
                    except:
                        pass
                elif "Unban:" in msg.text:
                    midd = msg.text.replace("Unban:","")
                    try:
                        del black["blacklist"][midd]
                        backupData()
                        cl.sendMessage(to, "已解除黑名單")
                    except:
                        pass
                elif text.lower() == 'read off':
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%Y') + " - " + bln + " - " + timeNow.strftime('%d') + "\n" + timeNow.strftime('%H:%M:%S')
                    if msg.to not in read['readPoint']:
                        cl.sendMessage(msg.to,"尚無已讀點")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        cl.sendMessage(msg.to, "刪除已讀點:\n" + readTime)
                elif text.lower() == 'read reset':
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%Y') + " - " + bln + " - " + timeNow.strftime('%d') + "\n" + timeNow.strftime('%H:%M:%S')
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        cl.sendMessage(msg.to, "重製已讀點\n" + readTime)
                    else:
                        cl.sendMessage(msg.to, "尚無已讀點")    
                elif text.lower() == 'read':
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%Y') + " - " + bln + " - " + timeNow.strftime('%d') + "\n" + timeNow.strftime('%H:%M:%S')
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            cl.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ 已讀者 ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ 已讀點設立時間 ]: \n" + readTime
                        try:
                            cl.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        cl.sendMessage(receiver,"請先設立已讀點")
                elif 'bj' in text.lower():
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == True:
                            G.preventedJoinByTicket = False
                            cl.updateGroup(G)
                        Ti = cl.reissueGroupTicket(to)
                        kicker01.acceptGroupInvitationByTicket(to, Ti)
                        kicker02.acceptGroupInvitationByTicket(to, Ti)
                        kicker03.acceptGroupInvitationByTicket(to, Ti)
                        G.preventedJoinByTicket = True
                        cl.updateGroup(G)
                elif text.lower() == 'bgbye':
                    if msg.toType == 2:
                        ginfo = cl.getGroup(to)
                        kicker01.leaveGroup(to)
                        kicker02.leaveGroup(to)
                        kicker03.leaveGroup(to)
                elif text.lower() == 'abye':
                    if msg.toType == 2:
                        ginfo = cl.getGroup(to)
                        kicker01.leaveGroup(to)
                        kicker02.leaveGroup(to)
                        kicker03.leaveGroup(to)
                        cl.leaveGroup(to)
                elif "Fbc:" in msg.text:
                    bctxt = text.replace("Fbc:","")
                    t = cl.getAllContactIds()
                    for manusia in t:
                        cl.sendMessage(manusia,(bctxt))
                elif "Gbc:" in msg.text:
                    bctxt = text.replace("Gbc:","")
                    n = cl.getGroupIdsJoined()
                    for manusia in n:
                        cl.sendMessage(manusia,(bctxt))
                elif "Ri " in msg.text:
                    Ri0 = text.replace("Ri ","")
                    Ri1 = Ri0.rstrip()
                    Ri2 = Ri1.replace("@","")
                    Ri3 = Ri2.rstrip()
                    _name = Ri3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                cl.kickoutFromGroup(to,[target])
                                cl.findAndAddContactsByMid(target)
                                cl.inviteIntoGroup(to,[target])
                            except:
                                pass
                elif "Uk " in msg.text:
                    midd = text.replace("Uk ","")
                    cl.kickoutFromGroup(to,[midd])
                elif "Tk " in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.kickoutFromGroup(to,[target])
                        except:
                            pass
                elif "Tkk " in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            klist = [kicker01,kicker02,kicker03]
                            kickers = random.choice(klist)
                            kickers.kickoutFromGroup(to,[target])
                        except:
                            pass
                elif "Mk " in msg.text:
                    Mk0 = text.replace("Mk ","")
                    Mk1 = Mk0.rstrip()
                    Mk2 = Mk1.replace("@","")
                    Mk3 = Mk2.rstrip()
                    _name = Mk3
                    gs = cl.getGroup(to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                cl.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Mkk " in msg.text:
                    Mkk0 = text.replace("Mkk ","")
                    Mkk1 = Mkk0.rstrip()
                    Mkk2 = Mkk1.replace("@","")
                    Mkk3 = Mkk2.rstrip()
                    _name = Mkk3
                    gs = cl.getGroup(to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                klist = [kicker01,kicker02,kicker03]
                                kickers = random.choice(klist)
                                kickers.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Nk " in msg.text:
                    _name = text.replace("Nk ","")
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                cl.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Nkk " in msg.text:
                    _name = text.replace("Nkk ","")
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                klist = [kicker01,kicker02,kicker03]
                                kickers = random.choice(klist)
                                kickers.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Zk" in msg.text:
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                cl.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Zkk" in msg.text:
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                klist = [kicker01,kicker02,kicker03]
                                kickers = random.choice(klist)
                                kickers.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Vk:" in text:
                    midd = msg.text.replace("Vk:","")
                    cl.kickoutFromGroup(msg.to,[midd])
                    cl.findAndAddContactsByMid(midd)
                    cl.inviteIntoGroup(msg.to,[midd])
                    cl.cancelGroupInvitation(msg.to,[midd])
                elif "Vk " in msg.text:
                        vkick0 = msg.text.replace("Vk ","")
                        vkick1 = vkick0.rstrip()
                        vkick2 = vkick1.replace("@","")
                        vkick3 = vkick2.rstrip()
                        _name = vkick3
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for s in gs.members:
                                if _name in s.displayName:
                                        targets.append(s.mid)
                        if targets == []:
                                cl.sendMessage(msg.to,"用戶不存在")
                                pass
                        else:
                                for target in targets:
                                        try:
                                                cl.kickoutFromGroup(msg.to,[target])
                                                cl.findAndAddContactsByMid(target)
                                                cl.inviteIntoGroup(msg.to,[target])
                                                cl.cancelGroupInvitation(msg.to,[target])
                                        except:
                                                pass
                elif text.lower() == 'zt':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            sendMessageWithMention(to,target)
                elif text.lower() == 'zm':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        mc = ""
                        for mi_d in targets:
                            mc += "->" + mi_d + "\n"
                        cl.sendMessage(to,mc)
                elif "Mc " in msg.text:
                    mmid = msg.text.replace("Mc ","")
                    cl.sendContact(to, mmid)
                elif "Sc " in msg.text:
                    ggid = msg.text.replace("Sc ","")
                    group = cl.getGroup(ggid)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "未找到"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                    ret_ += "\n╠ 群組網址 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif msg.text in ["c","C","cancel","Cancel"]:
                  if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    if X.invitee is not None:
                        gInviMids = (contact.mid for contact in X.invitee)
                        ginfo = cl.getGroup(msg.to)
                        sinvitee = str(len(ginfo.invitee))
                        start = time.time()
                        for cancelmod in gInviMids:
                            cl.cancelGroupInvitation(msg.to, [cancelmod])
                        elapsed_time = time.time() - start
                        cl.sendMessage(to, "已取消完成\n取消時間: %s秒" % (elapsed_time))
                        cl.sendMessage(to, "取消人數:" + sinvitee)
                    else:
                        cl.sendMessage(to, "沒有任何邀請")
                elif "Gn " in msg.text:
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"無法使用於副本")
                elif text.lower().startswith('ad:'):
                    if msg._from in admin5:
                        MENTION = eval(msg.contentMetadata['MENTION'])
                        inkey = MENTION['MENTIONEES'][0]['M']
                        admin.append(str(inkey))
                        cl.sendMessage(to, "已加入權限")
                        backupData()
                elif text.lower().startswith('ad5:'):
                    if msg._from in admin5:
                        MENTION = eval(msg.contentMetadata['MENTION'])
                        inkey = MENTION['MENTIONEES'][0]['M']
                        admin5.append(str(inkey))
                        cl.sendMessage(to, "已加入權限")
                        backupData()
                elif text.lower().startswith('ra:'):
                    if msg._from in admin5:
                        MENTION = eval(msg.contentMetadata['MENTION'])
                        inkey = MENTION['MENTIONEES'][0]['M']
                        admin.remove(str(inkey))
                        cl.sendMessage(to, "已刪除權限")
                        backupData()
                elif text.lower().startswith('ra5:'):
                    if msg._from in admin5:
                        MENTION = eval(msg.contentMetadata['MENTION'])
                        inkey = MENTION['MENTIONEES'][0]['M']
                        admin5.remove(str(inkey))
                        cl.sendMessage(to, "已刪除權限")
                        backupData()
                elif text.lower().startswith('mad:'):
                    if msg._from in admin5:
                        midd = msg.text.replace("mad:","")
                        admin.append(str(midd))
                        cl.sendMessage(to, "已加入權限") 
                        backupData()
                elif text.lower().startswith('mad5:'):
                    if msg._from in admin5:
                        midd = msg.text.replace("mad5:","")
                        admin5.append(str(midd))
                        cl.sendMessage(to, "已加入權限") 
                        backupData()
                elif text.lower().startswith('mra:'):
                    if msg._from in admin5:
                        midd = msg.text.replace("mra:","")
                        admin.remove(str(midd))
                        cl.sendMessage(to, "已刪除權限") 
                        backupData()
                elif text.lower().startswith('mra5:'):
                    if msg._from in admin5:
                        midd = msg.text.replace("mra5:","")
                        admin5.remove(str(midd))
                        cl.sendMessage(to, "已刪除權限") 
                        backupData()
                elif text.lower() == 'time':
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%Y') + " - " + bln + " - " + timeNow.strftime('%d') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    cl.sendMessage(msg.to, readTime)
                elif "Gc" in msg.text:
                    if msg.toType == 2:
                        key = eval(msg.contentMetadata["MENTION"])
                        u = key["MENTIONEES"][0]["M"]
                        contact = cl.getContact(u)
                        cu = cl.getProfileCoverURL(mid=u)
                        try:
                            cl.sendMessage(msg.to,"名字:\n" + contact.displayName + "\n\nMid:\n" + contact.mid + "\n\n個簽:\n" + contact.statusMessage + "\n\n頭貼網址 :\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n封面網址 :\n" + str(cu))
                        except:
                            cl.sendMessage(msg.to,"名字:\n" + contact.displayName + "\n\nMid:\n" + contact.mid + "\n\n個簽:\n" + contact.statusMessage + "\n\n封面網址:\n" + str(cu))
                elif "Inv " in msg.text:
                    midd = msg.text.replace("Inv ","")
                    cl.findAndAddContactsByMid(midd)
                    cl.inviteIntoGroup(msg.to,[midd])
                elif "Ban" in msg.text:
                    if msg.toType == 2:
                        print ("[Ban] 成功")
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    settings["blacklist"][target] = True
                                    cl.sendMessage(to, "已加入黑名單")
                                except:
                                    pass
                elif "Unban" in msg.text:
                    if msg.toType == 2:
                        print ("[UnBan] 成功")
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    del settings["blacklist"][target]
                                    cl.sendMessage(to, "已解除黑名單")
                                except:
                                    pass
                elif text.lower() == '/cb':
                    for mi_d in settings["blacklist"]:
                        settings["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                elif text.lower() == 'banlist':
                    if settings["blacklist"] == {}:
                        cl.sendMessage(to, "沒有黑名單")
                    else:
                        cl.sendMessage(to, "以下是黑名單")
                        mc = ""
                        for mi_d in settings["blacklist"]:
                            mc += "->" + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'alist':
                        mc = ""
                        for mi_d in admin:
                            mc += "•" + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'a5list':
                        mc = ""
                        for mi_d in admin5:
                            mc += "•" + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'a4list':
                        mc = ""
                        for mi_d in admin4:
                            mc += "•" + cl.getContact(mi_d).displayName + "\n"
                            cl.sendMessage(to, mc)
                elif text.lower() == 'banmid':
                    if settings["blacklist"] == {}:
                        cl.sendMessage(to, "沒有黑名單")
                    else:
                        cl.sendMessage(to, "以下是黑名單")
                        mc = ""
                        for mi_d in settings["blacklist"]:
                            mc += "->" + mi_d + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'kill ban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                        for tag in settings["blacklist"]:
                            matched_list+=filter(lambda str: str == tag, gMembMids)
                        if matched_list == []:
                            print ("1")
                            cl.sendMessage(to, "沒有黑名單")
                            return
                        for jj in matched_list:
                            cl.kickoutFromGroup(to, [jj])
                            cl.sendMessage(to, "黑名單以踢除")
                elif "/inv:" in msg.text:
                    gid = msg.text.replace("/inv:","")
                    if gid == "":
                        cl.sendMessage(to,"請輸入群組ID")
                    else:
                        try:
                            cl.findAndAddContactsByMid(msg.from_)
                            cl.inviteIntoGroup(gid,[msg.from_])
                        except:
                            cl.sendMessage(to,"我不在那個群組裡")
                elif msg.text in ["Friendlist"]:
                    anl = cl.getAllContactIds()
                    ap = ""
                    for q in anl:
                        ap += "• "+cl.getContact(q).displayName + "\n"
                    cl.sendMessage(msg.to," 朋友列表 \n"+ap+"人數 : "+str(len(anl)))
                elif text.lower() == 'bl':
                                blockedlist = cl.getBlockedContactIds()
                                kontak = cl.getContacts(blockedlist)
                                num=1
                                msgs="Blocked list:"
                                for ids in kontak:
                                    msgs+="\n[%i] %s" % (num, ids.displayName)
                                    num=(num+1)
                                msgs+="\n\n總共%i人" % len(kontak)
                                cl.sendMessage(msg.to, msgs)
                elif text.lower() == '@bg3sp':
                    start = time.time()
                    cl.sendMessage(to, "Please wait...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "seconds")
                elif text.lower() == 'update':
                	if msg._from in admin5:
                         cl.sendMessage(to, "Please wait....")
                         restartBot()
                elif text.lower() == 'gcel':
                    gid = cl.getGroupIdsInvited()
                    start = time.time()
                    for i in gid:
                        cl.rejectGroupInvitation(i)
                    elapsed_time = time.time() - start
                    cl.sendMessage(to, "All group invite cancel.")
                    cl.sendMessage(to, "取消時間: %s秒" % (elapsed_time))
                elif text.lower() == 'rt':
                    timeNow = time.time()
                    uptime = timeNow - botStart
                    uptime = format_timespan(uptime)
                    cl.sendMessage(to, "機器運行時間 {}".format(str(uptime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        creator = cl.getContact(BG)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於帳號 ]"
                        ret_ += "\n╠ 名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 封鎖 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於機器 ]"
                        ret_ += "\n╠ 版本 : mafu 個人版"
                        ret_ += "\n╠ 作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ MAFU 個人機 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))

                elif text.lower() == 'set':
                    try:
                        ret_ = "[ 設定 ]"
                        if settings["autoAdd"] == True: ret_ += "\n自動加入好友 ✅"
                        else: ret_ += "\n自動加入好友 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n自動加入群組 ✅"
                        else: ret_ += "\n自動加入群組 ❌"
                        if settings["autoJoinTicket"] == True: ret_ += "\n網址自動入群 ✅"
                        else: ret_ += "\n網址自動入群 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n自動離開副本 ✅"
                        else: ret_ += "\n自動離開副本 ❌"
                        if settings["inviteprotect"] == True: ret_ += "\n群組邀請保護 ✅"
                        else: ret_ += "\n群組邀請保護 ❌"
                        if settings["qrprotect"] == True: ret_ += "\n群組網址保護 ✅"
                        else: ret_ += "\n群組網址保護 ❌"
                        if settings["protect"] == True: ret_ += "\n群組保護 ✅"
                        else: ret_ += "\n群組保護 ❌"
                        if settings["contact"] == True: ret_ += "\n詳細資料 ✅"
                        else: ret_ += "\n詳細資料 ❌"
                        if settings["reread"] == True: ret_ += "\n查詢收回開啟 ✅"
                        else: ret_ += "\n查詢收回關閉 ❌"
                        if settings["detectMention"] == False: ret_ += "\n標註回覆開啟 ✅"
                        else: ret_ += "\n標註回覆關閉 ❌"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'add on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加友已開啟")
                elif text.lower() == 'add off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加友已關閉")
                elif text.lower() == 'join on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動入群已開啟")
                elif text.lower() == 'join off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動入群已關閉")
                elif text.lower() == 'leave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "自動離開副本已開啟")
                elif text.lower() == 'leave off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "自動離開副本已關閉")
                elif text.lower() == 'contact on':
                    settings["contact"] = True
                    cl.sendMessage(to, "好友資料開啟")
                elif text.lower() == 'contact off':
                    settings["contact"] = False
                    cl.sendMessage(to, "好友資料關閉")
                elif text.lower() == 'inviteprotect on':
                    settings["inviteprotect"] = True
                    cl.sendMessage(to, "邀請保護已開啟")
                elif text.lower() == 'inviteprotect off':
                    settings["inviteprotect"] = False
                    cl.sendMessage(to, "邀請保護已關閉")
                elif text.lower() == 'qr on':
                    settings["qrprotect"] = True
                    cl.sendMessage(to, "網址保護已開啟")
                elif text.lower() == 'qr off':
                    settings["qrprotect"] = False
                    cl.sendMessage(to, "網址保護已關閉")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to, "顯示收回開啟")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to, "顯示收回關閉")
                elif text.lower() == 'tag on':
                    settings["detectMention"] = True
                    cl.sendMessage(to, "標註提醒已開啟 ")
                elif text.lower() == 'tag off':
                    settings["detectMention"] = False
                    cl.sendMessage(to, "標註提醒已關閉")
                elif text.lower() == 'ck on':
                    settings["checkSticker"] = True
                    cl.sendMessage(to, "貼圖資料查詢已開啟")
                elif text.lower() == 'ck off':
                    settings["checkSticker"] = False
                    cl.sendMessage(to, "貼圖資料查詢已關閉")
                elif text.lower() == 'qrjoin on':
                    settings["autoJoinTicket"] = True
                    cl.sendMessage(to, "網址自動入群已開啟")
                elif text.lower() == 'qrjoin off':
                    settings["autoJoinTicket"] = False
                    cl.sendMessage(to, "網址自動入群已關閉")
                elif text.lower() == 'protect on':
                    gid = cl.getGroup(to)
                    settings["protect"] = True
                    cl.sendMessage(to, "群組保護已開啟")
                elif text.lower() == 'protect off':
                    gid = cl.getGroup(to)
                    settings["protect"] = False
                    cl.sendMessage(to, "群組保護已關閉")
                elif text.lower() == 'me':
                    cl.sendContact(to,str(msg._from))
                    cl.sendMessage(to,str(msg._from))
                elif text.lower() == 'mid':
                    cl.sendMessage(msg.to, sender)
                elif text.lower() == 'name':
                    me = cl.getContact(sender)
                    cl.sendMessage(msg.to, me.displayName)
                elif text.lower() == 'bio':
                    me = cl.getContact(sender)
                    cl.sendMessage(msg.to, me.statusMessage)
                elif text.lower() == 'picture':
                    me = cl.getContact(sender)
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'cover':
                    me = cl.getContact(sender)
                    cover = cl.getProfileCoverURL(sender)
                    cl.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif text.lower() == 'gcel':
                    gid = cl.getGroupIdsInvited()
                    start = time.time()
                    for i in gid:
                        cl.rejectGroupInvitation(i)
                    elapsed_time = time.time() - start
                    cl.sendMessage(to, "全部群組邀請已取消")
                    cl.sendMessage(to, "取消時間: %s秒" % (elapsed_time))
                elif "boom" in msg.text:
                        if msg.toType == 2:
                         start = time.time()
                         _name = msg.text.replace("boom","")
                         gs = cl.getGroup(to)
                         elapsed_time = time.time() - start
                         cl.sendMessage(to, "測試速度...")
                         cl.sendMessage(to, "%s秒" % (elapsed_time))
                         cl.sendMessage(to, "Kick all by Maizong")
                         targets = []
                         for g in gs.members:
                             if _name in g.displayName:
                                 targets.append(g.mid)
                         if targets == []:
                             pass
                         else:
                             for target in targets:
                                 if target in admin:
                                     pass
                                 else:
                                    try:
                                         klist=[cl]
                                         kicker=random.choice(klist)
                                         kicker.kickoutFromGroup(to, [target])
                                    except:
                                             pass
                elif "/inv:" in msg.text:
                    gid = msg.text.replace("/inv:","")
                    if gid == "":
                        cl.sendMessage(to,"請輸入群組ID")
                    else:
                        try:
                            cl.findAndAddContactsByMid(msg.from_)
                            cl.inviteIntoGroup(gid,[msg.from_])
                        except:
                            cl.sendMessage(to,"我不在那個群組裡")
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("name "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, contact.displayName)
                elif msg.text.lower().startswith("bio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, contact.statusMessage)
                elif msg.text.lower().startswith("picture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cover "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))
                elif text.lower() == 'gcreator':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'gid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, gid.id)
                elif text.lower() == 'gurl':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to,"https://line.me/R/ti/g/" + format(str(ticket)))
                        else:
                            cl.sendMessage(to, "網址關著".format(str(settings["keyCommand"])))
                elif text.lower() == 'urlon':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == False:
                            cl.sendMessage(to, "網址開啟中")
                        else:
                            G.preventedJoinByTicket = False
                            cl.updateGroup(G)
                            cl.sendMessage(to, "已開啟網址")
                elif text.lower() == 'urloff':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == True:
                            cl.sendMessage(to, "網址已關閉")
                        else:
                            G.preventedJoinByTicket = True
                            cl.updateGroup(G)
                            cl.sendMessage(to, "已關閉網址")
                elif text.lower() == 'ginfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "未找到"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                    ret_ += "\n╠ 群組網址 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 群組資料 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'gml':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員列表 ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 總共： {} ]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'glist':
                        groups = cl.groups
                        ret_ = "╔══[ 群組列表 ]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ 總共 {} 個群組 ]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "總共 {} 個成員".format(str(len(nama))))
        if op.type == 26:
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            cl.sendMessage(at,"%s收回了訊息\n訊息內容:\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            print ("[收回訊息]")
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == False:
                                    contact = cl.getContact(sender)
                                    cl.sendMessage(to, "下線中ˊˋ")
                                    sendMessageWithMention(to, contact.mid)
                                break
        if op.type == 55:
            print ("[ 55 ] 通知讀取消息")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
