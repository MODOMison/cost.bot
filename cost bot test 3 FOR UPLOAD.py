# Historical / Geographical Cost (using chatGPT)
import openai
from breezypythong_ui import EasyFrame

class GPTcost(EasyFrame):
    """
    User enters an item and a year and/or location.  Cost is looked up via
    query to chatGPT and result is displayed. Tries 3 times.
    """
   
    def __init__(self):  
        EasyFrame.__init__(self, title="cost.bot") #, width=500, height=500) # sticky = "NSEW")
        self["background"] = "Dark Red"

        # Label and fields for input  
        self.addLabel(text="Item (can be anything)",
                row=0, column=0, sticky="E")
        self.itemField = self.addTextField(text="", row=0, column=1, width=35, sticky="W")

        self.addLabel(text="Year and/or Location",
                row=1, column=0, sticky="E")
        self.yearField = self.addTextField(text="", row=1, column=1, width=35, sticky="W") #, height = 2, wrap="word")

        # Command button
        self.computeButton = self.addButton(text="Find Cost", row=2,
                column=1, command=self.askCost)
        self.computeButton.bind("<Return>", self.askCost)
       
        # Text area for results of prompt
        self.costField = self.addTextArea(text="", row=3,
                column=1, width=25, height=15, wrap="word") #, font=("Verdana",16)) # font="Verdana") #state="readonly")
       
        # Bind the "Tab" key to advance the cursor to the next field
        self.bind("<Tab>", self.advance_cursor)
       
    def askCost(self, event=None):
        """ Queries chatGPT with prompt """
       
        item = self.itemField.getText()
        year = self.yearField.getText()
        self.prompt = "How much did " + item + " cost in " + year + "?"
       
        self.costField.setText(self.GPTanswer())
               
    def GPTanswer(self):
        """
        Sends a prompt to chatGPT and returns response
        Tries 3 times to get a definitive answer
        """
        print("Prompt: ", self.prompt)  

        openai.api_key = "OMFG LOOK -> PLEASE WRITE YOUR API KEY HERE"
        model = "gpt-3.5-turbo"  # Use the model name for GPT-3.5

        """ repeat query up to 3 times if the reply is indefinite
            or 'cannot answer ' """
        ask_count = 0
        GPTanswer = "definitive"
        while ask_count < 3 and ("definit" in GPTanswer or \
                "cannot" in GPTanswer or "could not find" in GPTanswer):
            response = openai.ChatCompletion.create(
                    model=model,  # Use the 'model' parameter instead of 'engine'
                    messages=[
                        {"role": "user", "content": self.prompt}
                    ],
                    max_tokens=70,
                    temperature=0.5,
            )
            GPTanswer = response.choices[0].message['content'].strip()
            ask_count += 1
            print("Response", ask_count, ": ", GPTanswer)
       
        return GPTanswer
       
    def advance_cursor(self, event):   # Triggered by TAB key
        # Advances the cursor to the next field or button
        focus = self.getFocusOwner()
               
        # Check if the current focus is on a field or button
        if isinstance(focus, (EasyFrame.TextField, EasyFrame.Button)):
                   
            # Get a list of all the fields and buttons in the frame
            widgets = self.getAllComponents()
                   
            # Find the current focus in the list
            current_index = widgets.index(focus)
           
            # Advance to the next field or button in the list
            next_index = (current_index + 1) % len(widgets)
                               
            # Set the focus to the next field or button
            widgets[next_index].requestFocus()
 
def main():  
        """ Instantiates and pops up the window """
        GPTcost().mainloop()

if __name__ == "__main__":
        main()
