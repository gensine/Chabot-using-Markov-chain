import random 
import re 
from collections import defaultdict, Counter  

class MarkovChatbot:
    def __init__(self):
        # Dictionary to store word transitions (Markov Chain)
        self.chain = defaultdict(Counter)
        
        self.start_words = []

    def train(self, text):
        sentences = re.split(r'[.!?]', text)
        
        for sentence in sentences:
        
            sentence = sentence.strip().lower()
        
            if not sentence:
                continue
            
            words = re.findall(r'\b\w+\b', sentence)
            
            # Ensure there is more than one word
            if len(words) > 1:
                
                self.start_words.append(words[0])
                # Build Markov Chain transitions (word -> next word)
                for i in range(len(words) - 1):
                    current_word = words[i]
                    next_word = words[i + 1]
                    self.chain[current_word][next_word] += 1  # Count occurrences

    def generate_response(self, seed_word=None, max_length=20):
        if not self.chain or not self.start_words:
            return "I need more input to learn!"
        
        
        if seed_word and seed_word.lower() in ["hi", "hello", "hey"]:
            return "Hello! How can I help you today?"
        if seed_word and seed_word.lower() == "how" and "are" in self.chain[seed_word.lower()]:
            return "I'm fine, thank you!"
        if seed_word and seed_word.lower() == "tell" and "me" in self.chain[seed_word.lower()]:
            return "chicken ke maa ko kya bolte h chicken kemmmaaaaaa"
        if seed_word and seed_word.lower() == "what" and "do" in self.chain[seed_word.lower()]:
            return "Answering your questions!"
        
        
        if not seed_word or seed_word.lower() not in self.chain:
            seed_word = random.choice(self.start_words)
        else:
            seed_word = seed_word.lower()
        response = [seed_word] 
        
        for _ in range(max_length - 1):
            last_word = response[-1]
            
            if last_word in self.chain and self.chain[last_word]:
                # Select next word based on weighted probability
                next_word = random.choices(
                    list(self.chain[last_word].keys()), 
                    weights=self.chain[last_word].values()  
                )[0]
                
                
                if next_word != last_word:
                    response.append(next_word)
            else:
                break  
        
        # Convert response list into a sentence, capitalize first letter, and add a period
        return ' '.join(response).capitalize() + '.'

if __name__ == "__main__":
    bot = MarkovChatbot()  # Create chatbot instance
    
    dataset = (
        "Hello there! How are you today? I am a chatbot learning from our conversations. "
        "Let's talk about something interesting. What do you like to do for fun?"
    )
    bot.train(dataset)  
    
    print("Chatbot: Hello! Let's chat. Type 'exit' to end.")
    
    while True:
        user_input = input("You: ").strip()  
        
        if not user_input:
            print("Chatbot: Please say something!")
            continue
        
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break 
        
        bot.train(user_input)  
        
        # Use first word of user input as seed for response generation
        seed_word = user_input.split()[0]
        response = bot.generate_response(seed_word)
        
        print(f"Chatbot: {response}")  # Print chatbot response
