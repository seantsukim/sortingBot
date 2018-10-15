#Sean Kim's Sorting Hat Discord Bot
#Client ID: 431331129988218890
#LTYqwEyg0jYFGUPc7tbjLeCWIK-vZVhr
#Authorization URL: https://discordapp.com/oauth2/authorize?scope=bot&permissions=o&client_id=431331129988218890
#Sorting Hat#4538
#Token: NDMxMzMxMTI5OTg4MjE4ODkw.DadMNw.nn4Kd-xMnaoqNGp0wycleLlClGM

#To set up the bot, there needs to be an Admin role in the server (faction maker).
#then call makefactions for the four roles that you want to assign in the server (or use the default ones if your like)
#All set, questions are permanent unless the creator (Sean Kim) changes them

from discord import Game
from discord.ext.commands import Bot
from discord.utils import get

#Sorting Hat's token to run
token = 'NDMxMzMxMTI5OTg4MjE4ODkw.DadMNw.nn4Kd-xMnaoqNGp0wycleLlClGM'

#The way for users to call on the bot's functions
hat = Bot(command_prefix = '!')

faction_name1 = 'Holy'
faction_name2 = 'Vigilant'
faction_name3 = 'Hunter'
faction_name4 = 'Destroyer'

@hat.event
async def on_ready():
    '''
    Shows that the bot's running when we run this program.
    '''
    await hat.change_presence(game = Game(name = 'with Dumbledore'))
    print("Bot Logging In!")
    print("Bot ID: " + hat.user.id)
    print(hat.user.name + " is ready!")

@hat.command(pass_context = True)
async def makefactions(context, role1: str, role2:str, role3:str, role4:str):
    '''
    a discord command that allows admin to change to roles the bot assigns.
    only needs to be called once, incase this bot is in a foreign server where roles
    are not the same as the global variables.
    '''
    #if someone who isn't admin is trying to use command
    if not(is_admin(context)):
        await hat.say("I'm afraid I cannot let you do that.")
        return
    else:
        faction_name1 = role1
        faction_name2 = role2
        faction_name3 = role3
        faction_name4 = role4
        await hat.say("Done! New factions are (in order): {}, {}, {}, and {}.".format(
            role1, role2, role3, role4))
        
    
@hat.command(name = 'showquiz',
             aliases = ['ShowQuiz', 'SHOWQUIZ', 'ShowForm'],
             pass_context = True)
async def showquiz(context):
    '''
    Quiz form for server.
    This will show the quiz that one must answer to be admitted into a certain
    server faction.
    '''
    num_q = 4 #number of questions in case we need to change anything in the quiz

    #Beginning of the quiz form
    quiz = "There will be {} questions for one to answer, please answer with \
a, b, c, d, e for each question when you !takequiz to determine what server faction \
you shall be.\n\n".format(num_q)
    
    #Question 1
    quiz +="Question 1 \nWhat is your favorite color? \n\
a)Red b)Blue c)Yellow d)Green e)Other \n\n"
    
    #Question 2
    quiz +="Question 2 \nWhat type of music do you like? \n\
a)Pop b)Rock c)EDM d)Country e)Other \n\n"
    
    #Question 3
    quiz +="Question 3 \nWhat pet do you own? \n\
a)Dog b)Cat c)Bird d)Lizard e)Other \n\n"
    
    #Question 4
    quiz +="Question 4 \nWhat is your favorite flavor of ice cream? \n\
a)Chocolate b)Vanilla c)Rocky Road d)Cookies and Cream e)Other \n\n"

    await hat.say(quiz) #shows form to the server

def check_answer(check:str):
    '''
    Helper function for the hat's takequiz call.
    Makes sure that answers are all either a, b, c, d, or e.
    Possible answers for the quiz.
    '''
    return (check == 'a' or check == 'b' or check == 'c' or\
            check == 'd' or check == 'e')

def faction_score(q1:str, q2:str, q3:str, q4:str):
    '''
    Helper function for the hat's takequiz call.
    This function will take in the answers on the quiz form,
    Returning a quiz score to determine the faction the member will be.
    '''
    q_form = ['q1', 'q2', 'q3', 'q4'] #quiz questions
    ans_q = [q1, q2, q3, q4] #quiz answers given in
    ans_score = {'q1': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 0},
                 'q2': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 0},
                 'q3': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 0},
                 'q4': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 0}} #quiz score dictionary
    quiz_score = 0 #total quiz score to return
    
    for q_num in range(len(q_form)): #iterates from 0 - n, to pull questions and answers
        quiz_score += ans_score[q_form[q_num]][ans_q[q_num]] #adds to the total score

    return quiz_score

def det_faction(score:int):
    '''
    Helper function for the hat's takequiz call.
    This function takes the faction score in,
    Returning the faction determined by the score intaken.
    '''
    factions = ['A', 'B', 'C', 'D'] #factions possibly given
    index = 999 #factions index to pick in

    if (score < 4):
        index = 0
    elif (4 <= score < 8):
        index = 1
    elif (8 <= score < 12):
        index = 2
    else:
        index = 3

    return factions[index]
    

@hat.command(name = 'takequiz',
             aliases = ['TakeQuiz', 'Takequiz', 'TAKEQUIZ'],
             pass_context = True)
async def takequiz(context, q1='x', q2='x', q3='x', q4='x'):
    '''
    Submit answers to quiz here if you are a new member.
    Put your answers a-e for all the questions after !takequiz to get your results.
    Answers are not case-sensitive.
    '''
    #If the member is already aligned to a faction/role
    if (len(context.message.author.roles) != 1) and (not(is_admin(context))):
        await hat.say("I'm sorry you were already admitted into a faction.")
        return

    #If the member forgets an answer when submitting their answers
    if (q1 == 'x' or q2 == 'x' or q3 == 'x' or q4 == 'x'):
        await hat.say("I'm sorry, you seemed to have forgotten an answer.")
        return
    
    #If the member tries to add an answer other than a, b, c, d, or e
    if not(check_answer(q1.lower()) and check_answer(q2.lower()) and\
           check_answer(q3.lower()) and check_answer(q4.lower())):
        await hat.say("I'm sorry, one of your answers isn't appropriate for the quiz.")
        return

    #calculates faction score and processes member's alignment
    align_score = faction_score(q1, q2, q3, q4)
    alignment = det_faction(align_score)

    member = context.message.author

    #based on score, determines server faction
    if alignment == 'A':
        role = get(member.server.roles, name = faction_name1)
    elif alignment == 'B':
        role = get(member.server.roles, name = faction_name2)
    elif alignment == 'C':
        role = get(member.server.roles, name = faction_name3)
    elif alignment == 'D':
        role = get(member.server.roles, name = faction_name4)
    else:
        print("uh-oh, that shouldn't have happened")
    
    await hat.say('Through your answers you have been placed into the {} faction!'.format(role))
    await hat.add_roles(member, role)

def is_admin(context):
    '''
    checks the context to see if the individual is an admin
    '''
    return "admin" in [role.name.lower() for role in context.message.author.roles]

hat.run(token)
