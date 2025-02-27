# Ari-Living-Framework

What this project is:
This is an ongoing experiment in creating an AI framework involving memory, continuity, and adpation that will shape how AI learns and generates ideas. 
Currently I have a memory system intended to be integrated in LLMs, but right now it functions on its own but in my base model I am using.
The current set up is Mistral 7B base v3 with no fine tuning, but I intend to fine tune on fundamental skills to create a backbone for growth organically. 

Current problem: The base model currently struggles eith using the memory efficiently without fine tuning which is causing endless looping.  Without basic understanding of context,
the base model will loop responses over and over and add memory with no understanding of the weighting system. 

Next steps: Fine tuning on small datasets to teach the model how to utilize memory and basic learning and communicating skills using loRA.
