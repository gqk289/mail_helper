#-*- encoding: utf-8 -*-    
  
#导入smtplib和MIMEText  
import smtplib  
from email.Header import Header  
from email.MIMEText import MIMEText  
from email.MIMEMultipart import MIMEMultipart  
import os.path  
  
def mailtest(from_addr,to_addr,subject,content,attfile,smtp_server,passwd):  
    #创建一个带附件的实例  
    msg = MIMEMultipart()  
  
    #添加邮件内容  
    #注意，要指定邮件内容的编码为utf-8，否则中文会有乱码  
    text_msg = MIMEText(content,'plain','utf-8')  
    msg.attach(text_msg)  
      
    #构造附件  
    #注意：传入的参数attfile为unicode，否则带中文的目录或名称的文件读不出来  
    #      basename 为文件名称，由于传入的参数attfile为unicode编码，此处的basename也为unicode编码  
    basename = os.path.basename(attfile)  
      
    #注意：指定att的编码方式为gb2312  
    att = MIMEText(open(attfile, 'rb').read(), 'base64', 'gb2312')  
    att["Content-Type"] = 'application/octet-stream'  
      
    #注意：此处basename要转换为gb2312编码，否则中文会有乱码。  
    #      特别，此处的basename为unicode编码，所以可以用basename.encode('gb2312')  
    #            如果basename为utf-8编码，要用basename.decode('utf-8').encode('gb2312')  
    att["Content-Disposition"] = 'attachment; filename=%s' % basename.encode('gb2312')  
    msg.attach(att)  
   
    #加邮件头  
    msg['to'] = to_addr  
    msg['from'] = from_addr  
    #主题指定utf-8编码，否则中文会有乱码  
    msg['subject'] = Header(subject, 'utf-8')
    password = passwd
      
    #发送邮件  
    server = smtplib.SMTP(smtp_server)
    server.login(from_addr,password)
    server.sendmail(msg['from'], msg['to'],msg.as_string())  
    server.close
  
