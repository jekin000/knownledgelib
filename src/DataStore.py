import traceback

def isDuplicate(logger,url):
    try:
        with open('urls.txt','r') as f:
            urls = f.readlines()
            for u in urls:
                if u.strip() == url:
                    return True
        f.close()
        with open('urls.txt','a') as f:
            f.write(url+'\n')
            return False
    except:
        logger.error(traceback.print_exc())
    return False

def implode(strlist,item):
    count = len(strlist)
    if count == 1:
        return strlist[0]

    retval = strlist[0]
    for i in range(1,count):
        retval = retval + item + strlist[i]
    
    return retval

def save(logger,key,vals):
    vstr = implode(vals,',')
    try:
        with open('output.txt','a') as f:
            f.write(key+'|'+vstr+'\n')
    except:
        logger.error(traceback.print_exc())
 
    logger.info('Save '+key+'|'+vstr)
    return
