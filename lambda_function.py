import os
import json
import openai
import time
import requests
from openai import OpenAI

def lambda_handler(event, context):
   
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assistant_id = os.getenv("ASSISTANT_ID")

    DATABASE_URL = 'https://insumos-veterinarios-default-rtdb.firebaseio.com/productos.json'
    
    def get_data_from_database():
        """Obtiene datos de la base de datos de Firebase."""
        response = requests.get(DATABASE_URL)
        return response.json()

    def buscar_producto(nombre_producto):
        """
        Busca un producto por nombre.
        
        :param nombre_producto: El nombre del producto a buscar.
        :return: El producto si se encuentra, o "Producto no encontrado" si no se encuentra.
        """
    
        data = get_data_from_database()
        nombre_producto = nombre_producto.upper()
        for producto in data:
            nombre_en_producto = producto['nombre'].upper()
            if nombre_producto in nombre_en_producto:
                return producto
        return "Producto no encontrado."

    def update_product_existence(nombre_producto, additional_existence,opcion):
        """
        Actualiza la existencia de un producto y envía los datos actualizados a Firebase.
        
        :param nombre_producto: El nombre del producto a actualizar.
        :param additional_existence: La cantidad a agregar a la existencia actual.
        :param data: Los datos de los productos.
        :return: El código de estado de la respuesta HTTP, si la actualización fue exitosa. None en caso contrario.
        """
        data = get_data_from_database()
        nombre_producto = nombre_producto.upper()
        for producto in data:
            nombre_en_producto = producto['nombre'].upper()
            if nombre_producto in nombre_en_producto:
                current_existence = int(producto['existencias']) if producto['existencias'].isdigit() else 0
                if opcion == "mas":
                    producto['existencias'] = str(current_existence + int(additional_existence))
                elif opcion == "menos":
                    producto['existencias'] = str(current_existence - int(additional_existence))    
                
                # Envía los datos actualizados a Firebase
                response = requests.put(DATABASE_URL, data=json.dumps(data))
                return response.status_code
        return None
        
        
    def update_product_price(nombre_producto, new_price):
        """
        Actualiza el precio de un producto y envía los datos actualizados a Firebase.
        
        :param nombre_producto: El nombre del producto a actualizar.
        :param new_price: El nuevo precio del producto.
        :param data: Los datos de los productos.
        :return: El código de estado de la respuesta HTTP, si la actualización fue exitosa. None en caso contrario.
        """
        data = get_data_from_database()
        nombre_producto = nombre_producto.upper()
        for producto in data:
            nombre_en_producto = producto['nombre'].upper()
            if nombre_producto in nombre_en_producto:
                producto['precioVenta'] = str(new_price)
                
                # Envía los datos actualizados a Firebase
                response = requests.put(DATABASE_URL, data=json.dumps(data))
                return response.status_code
        return None        
    
    # OpenAI client initialization

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("Successful connection with OPENAI API ----------")
    except Exception as e:
        print(f"Error trying to connect: {e} -----------")

    # -------------------------------------------------------------------------------------------
        
    response = "no data"    


    def start_conversation():
        thread = client.beta.threads.create()
        thread_id = thread.id
        return thread_id 


    def chat(thread_id,user_input ):

        if not thread_id:
            return print("Error: thread_id is required")

        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(run_status.status)

            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                response = messages.data[0].content[0].text.value
                print(response)
                return response
                break

            elif run_status.status == 'requires_action':
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "buscar_producto":
                        arguments = json.loads(tool_call.function.arguments)
                        output = buscar_producto(arguments["nombre_producto"])
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread_id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(output)
                            }]
                        )

                    elif tool_call.function.name == "update_product_existence":
                        arguments = json.loads(tool_call.function.arguments)
                        output = update_product_existence(arguments["nombre_producto"],arguments["additional_existence"],arguments["opcion"])
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread_id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(output)
                            }]
                        ) 
                        
                    elif tool_call.function.name == "update_product_price":
                        arguments = json.loads(tool_call.function.arguments)
                        output = update_product_price(arguments["nombre_producto"],arguments["new_price"])
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread_id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(output)
                            }]
                        ) 

            time.sleep(1)


    thread_id = start_conversation()

    entrada_usuario = event["message_input"]
    response = chat(thread_id, entrada_usuario)
   
   
   
   
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }   