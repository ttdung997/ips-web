import sys
sys.path.insert(0,"/var/log/core_waf/") # uncomment
import re
import threading
import base64
import sys
import time
import datetime
import connect_db
# import Quinh

audit_log_path = '/var/log/apache2/modsec_audit.log' # uncomment
#audit_log_path = './modsec_audit.log' # remove


class Parser(threading.Thread):
    def __init__(self, mysql, audit_log_path):
        threading.Thread.__init__(self)
        try:
            self.audit_log_path = audit_log_path
            self.logs_file = open(self.audit_log_path, 'r')
            self.logs_file.seek(0, 2)
            self.last_size = self.logs_file.tell()
            self.logs_file.close()

            self.block_size = None
            self.current_size = None
            self.new_logs = None
            self.mysql = mysql
        except IOError:
            print "Can not find audit log file"
            sys.exit(1)
        pass

    def run(self):
        print "[Info] - Start monitor logs file..."
        while True:
            # get current file size
            self.logs_file = open(self.audit_log_path)
            self.logs_file.seek(0, 2)
            self.current_size = self.logs_file.tell()
            print self.last_size

            # if current_size > last_size, get block of new logs and parser it
            if self.current_size > self.last_size:
                print "[Info] - Detect new logs entry"
                self.logs_file.seek(self.last_size)
                
                self.block_size = self.current_size - self.last_size
                self.new_logs = self.logs_file.read(self.block_size)

                # set last_size = current_size
                self.last_size = self.current_size

                # parser new logs
                self.parser_log(self.new_logs)

            self.logs_file.close()
            time.sleep(10)
        pass

    def lookup_ip(self, ip):
        try:
            match = geolite2.lookup(ip)
            return short2long[match.country]
        except:
            return "Other"    

    def insert(self,query):
        #insert
        try:
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.db.commit()
            return True
        except:
            return False

    def parser_log(self, logs):
        # try:
        if 1:
            logs = re.findall('--[a-z0-9]+-A--\n(.*?)\n--[a-z0-9]+-Z--', logs, re.DOTALL)

            # parser all log raws
            for log in logs:
                # get date time 
                a_element = re.search('(.+)--[a-z0-9]+-B--', log, re.DOTALL)
                a_element = str(a_element.group())
                date_time = re.search('\[[a-zA-Z0-9:/]+\s', a_element)

                attack_ip = re.findall(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', a_element)
                attack_ip = attack_ip[0]
                print attack_ip
                attack_time = date_time.group()[1:-1]
                dict_month = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dev=12)
                attack_time = attack_time[:3] + str(dict_month[attack_time[3:6]]) + attack_time[6:]
                print '----------\n'
                print 'attack_time: '+attack_time+"\n"
                print '----------\n'
                attack_time = time.mktime(datetime.datetime.strptime(attack_time, "%d/%m/%Y:%H:%M:%S").timetuple())
                print '----------\n'
                print 'attack_time_22222: '+str(attack_time)+"\n"
                print '----------\n'
                # get domain & attack ip % country
                b_element = re.search('--[a-z0-9]+-B--(.*?)\n\n', log, re.DOTALL)
                b_element = str(b_element.group())
                domain = re.search('Host:\s(.*?)\n', b_element)
                domain = domain.group()[6:-1].split(':')[0]

                # attack_ip = re.search('X-Forwarded-For:\s(.*?)\n', b_element)
                country = "Other" # default contry if there are no X-Forwarded-For field in req-header
                if attack_ip:
                    # attack_ip = attack_ip.group()[17:-1]
                    country = self.lookup_ip(attack_ip)
                # country = "Vietnam"

                # link = re.search('\w{3,}\s(.*?)\n', b_element)
                # link = link.group()[:-1]

                # get request header -- for futher deverlovement
                requestheader = re.search('-\n\w{3,}(.*?)\n\n', b_element, re.DOTALL)
                c_element = re.search('--[a-z0-9]+-C--\n(.*?)\n', log, re.DOTALL)
                if c_element is None:
                    requestheader = (requestheader.group()[2:-2])
                else:
                    c_element = str(c_element.group())
                    payload = re.search('\n.(.*?)\n', c_element, re.DOTALL)
                    payload = payload.group()[1:-1]
                    requestheader = (requestheader.group()[2:] + payload) 

                print domain
                # get website id
                cursor = mysql.cursor()
                sql = "SELECT id, group_website_id FROM mod_website WHERE name =\'"+ domain +"\'"
                try:
                    cursor.execute(sql)
                    data = cursor.fetchall()
                except Exception,e :
                    mysql.rollback()
                    print e
                website_id = ''
                if data is None:
                    print "none"
                    continue 
                if len(data) == 0: 
                    print '1zero'
                    data = [[6, 3]]
                    # continue
                print data[0][1]
                website_id = str(data[0][0])
                group_website = str(data[0][1])


                # get all group_rule_id in database:
                cursor = mysql.cursor()
                sql = "SELECT id FROM mod_group_rule"
                try:
                    cursor.execute(sql)
                    data = cursor.fetchall()
                except Exception,e :
                    mysql.rollback()
                    print e
                if data is None:
                    print "none"
                    continue 
                if len(data) == 0: 
                    print '3zero'

                    # continue
                # print data
                group_rule_ids = [int(x[0]) for x in data]

                # get group_rule id
                h_element = re.search('--[a-z0-9]+-H--(.+)\n', log, re.DOTALL)
                h_element = str(h_element.group())
                all_messages = re.findall('(Message:.+)\n', h_element)
                group_rules = []
                # test
                rule_detail = []
                # test
                for message in all_messages:
                    severity = re.search('\[severity \"(\w+)\"\]', message)
                    if severity:
                        severity = severity.group(1)
                        if severity != "CRITICAL": continue
                    else: continue
                    # paranoia_level = re.search('\[tag \"paranoia-level\/(\w+)\"\]', message)
                    # if paranoia_level:
                    #     paranoia_level = int(paranoia_level.group(1))
                    #     if paranoia_level < 4: continue
                    # else: continue

                    rule_id = re.search('\[id \"(\d+)\"\]', message)
                    if rule_id: rule_id = rule_id.group(1)
                    else: continue
                    
                    group_rule = re.search('\[file \"\/.+\/[^\/]+.*-(\d*)-.*\.conf\"\]', message)
                    if group_rule: group_rule = group_rule.group(1)
                    else: continue
                    # group_rule = int(re.search('\[file \"\/.+\/[^\/]+.*-(\d*)-.*\.conf\"\]', message).group(1)) % 14 #remove
                    if (int(group_rule) not in group_rule_ids): continue
                    if (int(group_rule) in group_rules): continue
                    group_rules.append(int(group_rule))

                    # test
                    print "[!] test"
                    msg_type = re.search(r'Message: (\w*?)\.', message)
                    if msg_type: msg_type = msg_type.group(1)
                    # else: continue

                    data_matched_info = re.search(r'\[data \"Matched Data: (.*?) found within ([A-Z_]*?):(.*?)\"\]', message)
                    if data_matched_info: data_matched_info = data_matched_info.group()[7:-1]
                    # else: continue
                    print data_matched_info
                    rule_detail.append({'MSG_TYPE' : msg_type, 'group_rule' : group_rule, 'data' : data_matched_info})
                    print "[!] end test"
                    # test
                    
                if len(group_rules) == 0: continue
                group_rules = ','.join(str(x) for x in group_rules)#remove
                # group_rules = ','.join(x for x in group_rules)

                # insert into database
                from base64 import b64encode
                arr_event = (attack_ip, attack_time, country, group_website, website_id, group_rules, b64encode(requestheader), b64encode(str(rule_detail)))
                # query = """INSERT INTO monitor_waf_detail (timestamp, ip, contry, action, websites_waf_id, website_id, group_rule_id) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % arr_event[:-2]
                query = """INSERT INTO monitor (ip, time, country, group_website, website, group_rule, request_header, match_info) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')""" % arr_event
                print query
                cursor = mysql.cursor()
                try:
                    cursor.execute(query)
                    mysql.commit()
                except Exception,e :
                    mysql.rollback()
                    print e
                # print mysql.insert(query)
                
                print "------- [LogInfo] ------- "
                event_info = zip(('ip', 'time', 'country', 'group_website', 'website_id', 'group_rule_id', 'requestheader', 'detail'), arr_event)
                print "[+] event_info"
                for key in event_info:
                    if key[0] == 'detail':
                        print "\t[+]", key[0]
                        print "\t\t[-]", key[1]
                    else:                        
                        print "\t[+]", key[0], ":", str(key[1])[:32]
                print "-------------------------"
            
        # except Exception, e:
        #      raise e
        # pass

if __name__ == '__main__':
    import os
    # sys.path.insert(0,"/home/ubuntu/anhtvd/waf-log-monitor/") # uncomment
    mysql = connect_db.connect()
    # mysql = mysql.cursor()
    if os.path.isfile(audit_log_path):
        parser = Parser(mysql, audit_log_path)
        parser.start()
    pass

    # parser = Parser(mysql, audit_log_path)
    # f = open('./modsec_audit.log')
    # logs = f.read()
    # f.close()
    # # print logs
    # parser.parser_log(logs)
