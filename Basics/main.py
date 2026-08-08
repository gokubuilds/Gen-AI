from Basics.clienttest import llm_call
import streamlit as st
while True:
    query=input("enter the prompt:")

    if query=="e":
        break
    else:
        print(llm_call(query))
    