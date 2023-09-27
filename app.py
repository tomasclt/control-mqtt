import paho.mqtt.client as paho
import time
import streamlit as st
import json

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="157.230.214.127"
port=1883
client1= paho.Client("GIT-HUB")
client1.on_message = on_message
values =0.0


st.title("MQTT Control")

if st.button('ON'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)    
    message =json.dumps({"Act1":"ON","Analog": float(values)})
    ret= client1.publish("cmqtt", message)
    #client1.subscribe("Sensores")
    
else:
    st.write('')

if st.button('OFF'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)                                    
    message =json.dumps({"Act1":"OFF","Analog": float(values)})
    ret= client1.publish("cmqtt", message)
    
else:
    st.write('')

values = st.slider('Selecciona el rango de valores',0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("cmqtt", message)
 
else:
    st.write('')




