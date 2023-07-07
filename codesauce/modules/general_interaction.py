#!/usr/bin/python3

# Imports
from time import sleep
from codesauce.utils.colors import Color
from codesauce.modules.interaction import Interaction


class GeneralInteraction(Interaction):
    def interact(self, messages):
        max_retry = 7
        retry = 0
        while True:
            try:
                response = self.openai_api.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    temperature=self.temperature,
                )

                Color.print("\n{B}Answer: \n")
                chat = []
                for chunk in response:
                    delta = chunk["choices"][0]["delta"]
                    msg = delta.get("content", "")
                    print(msg, end="")
                    chat.append(msg)
                print()

                chat_response = {"role": "assistant", "content": "".join(chat)}
                self.chat_history.append(chat_response)
                break

            except Exception as oops:
                print(f'\n\nError communicating with OpenAI: "{oops}"')
                if "maximum context length" in str(oops):
                    self.chat_history.pop(0)
                    print("\n\n DEBUG: Trimming oldest message")
                    continue
                retry += 1
                if retry >= max_retry:
                    print(f"\n\nExiting due to excessive errors in API: {oops}")
                    exit(1)
                print(f"\n\nRetrying in {2 ** (retry - 1) * 5} seconds...")
                sleep(2 ** (retry - 1) * 5)

        return self.chat_history
