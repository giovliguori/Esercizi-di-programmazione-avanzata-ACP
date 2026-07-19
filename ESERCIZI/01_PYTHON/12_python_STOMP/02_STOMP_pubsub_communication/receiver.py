import time
import stomp
    

class MyListener(stomp.ConnectionListener):
    
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        print('received a message')
        print('text: "%s"' % frame.body)
        print('headers: "%s"' % frame.headers)
        print('cmd: "%s"' % frame.cmd)

if __name__ == "__main__":
    
    conn = stomp.Connection([('127.0.0.1', 61613)])
    #conn = stomp.Connection([('127.0.0.1', 61613)], auto_content_length=False) # To use to send TextMessage to a JMS-based application

    conn.set_listener('', MyListener(conn))

    conn.connect(wait=True)
    
    conn.subscribe(destination='/topic/mytesttopic', id=1, ack='auto')  # creazione di un subscriber non-durable (default)
     
                                                                        # Note: specify the physical name after /topic or /queue when used 
                                                                        # to send TextMessage to a JMS-based application

    print('Receiver waiting for messages...')

    time.sleep(60)

    conn.disconnect()

