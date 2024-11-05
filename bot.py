from openai import OpenAI
import os
import pickle as pkl
import argparse


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

FEATURE_CONTEXT_MAPPING = {}

with open('context_data/intent_system_msg.txt', 'r') as file:
    INTENT_SYSTEM_MSG = file.read()

with open("context_data/answerflow.txt", "r") as file:
    FEATURE_CONTEXT_MAPPING["answerflow"] = file.read()

with open("context_data/smart_block.txt", "r") as file:
    FEATURE_CONTEXT_MAPPING["smart_block"] = file.read()

with open("context_data/co_pilot.txt", "r") as file:
    FEATURE_CONTEXT_MAPPING["co_pilot"] = file.read()

with open("context_data/spark.txt", "r") as file:
    FEATURE_CONTEXT_MAPPING["spark"] = file.read()


def intent_classification(
        query:str,
        client:OpenAI,
        model_name:str,
        history:list=[]
        ):
    """
    This method is used to classify the intent behind the asked features.
    """
    res =  client.chat.completions.create(
        model= model_name,
        messages = [ {
                "role":"system",
                "content":INTENT_SYSTEM_MSG
            }] + history +
            [
            {
                "role":"user",
                "content":query
            },
            ],
        )
    
    return res.choices[0].message.content

def generation(
        query:str,
        client:OpenAI,
        model_name:str,
        history:list=[],
        sys_prompt:str = ""
        ):
    
    """
    This method is used to generate a response based on the given context.
    """

    res =  client.chat.completions.create(
        model= model_name,
        messages = [{
                "role":"system",
                "content":sys_prompt
            }]+ history + [
            {
                "role":"user",
                "content":query
            },
            ],
        )
    
    return res.choices[0].message.content
    
def main(client,model_name):
    history = []
    username = input("Enter your name: ")
    print("Press Ctrl+C to stop the program.")
    try:
        while True:
            query = input("\nEnter yor query: ")
            history.append({"role": "system", "content": INTENT_SYSTEM_MSG})
            history.append({"role": "user", "content": query})
            # feature classification

            first_response = intent_classification(query, client=client, model_name=model_name, history=history).lower()
            # handle unrelated query
            if len(first_response.split(" ")) > 1:
                print("Output from the Intent Block: ")
                print(first_response)
                history.append({"role": "assistant", "content": first_response})
                continue
            
            history.append({"role": "assistant", "content": first_response})

            # generate answer

            with open('context_data/generation_system_msg.txt', 'r') as file:
                GENERATION_SYSTEM_MSG = file.read()

            GENERATION_SYSTEM_MSG = GENERATION_SYSTEM_MSG.format(FEATURE_CONTEXT_MAPPING[first_response])
            history.append({"role": "system", "content": GENERATION_SYSTEM_MSG})

            second_response = generation(query, client=client, model_name=model_name, history=history,sys_prompt=GENERATION_SYSTEM_MSG)
            history.append({"role": "assistant", "content": second_response})
            print(second_response)

    except KeyboardInterrupt:
        with open(f"history/{username}.pkl", "wb") as file:
            pkl.dump(history, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="It takes model name from the user.")

    # Add an argument with a default value
    parser.add_argument("--model_name", 
                        type=str, 
                        default="gpt-4o",
                        help="The name of the OpenAI model.")

    client = OpenAI()

    args = parser.parse_args()

    main(client=client,model_name=args.model_name)







