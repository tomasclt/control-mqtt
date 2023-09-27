import paho.mqtt.client as paho
import time
from IPython.display import Audio
import streamlit as st
import threading
import queue

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)
    if(message_received=="Sonido"):
       sound_file = 'hum_high.mp3'
       display(Audio(sound_file, autoplay=True))
        


broker="157.230.214.127"
port=1883
client1= paho.Client("GIT-HUB")
client1.on_message = on_message



st.title("MQTT Control")


if st.button('ON'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)                                 
    ret= client1.publish("deteccion","ON") 
    client1.subscribe("Sensores")
    
else:
    st.write('')

if st.button('OFF'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)                                 
    ret= client1.publish("deteccion","OFF")
    client1.subscribe("Sensores")
    
else:
    st.write('')

values = st.slider('Selecciona el rango de valores',0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)                                 
    ret= client1.publish("deteccion", values)
 
    
else:
    st.write('')
