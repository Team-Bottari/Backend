import time

def request_parse(request):
    return f"\tMethod : {request.method}\n\t여기에서 : {request.client.host}:{request.client.port}\n\t여기로 : {request.url}",time.time()

def response_parse(response):
    return f"\t응답코드 : {response.status_code}\n\t결과타입 : {response.headers['content-type']}",time.time()

def make_log(start_log,end_log,start_time,end_time):
    return start_log+"\n"+end_log+f"\n\t처리시간 : {str(end_time-start_time)[:7]}"