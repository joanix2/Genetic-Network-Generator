import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import gauss as rg
import math

# Création d'un objet neurone
class Perceptron(): #hérite d'un objet noeu de graph dans la librairie pytorch
    def __init__(self, life:float, inputDict:dict = {}, outputVal:float = 0, isInput:bool = False, isOutput:bool = False, bias = 0):
        self.life = life
        self.start_life = self.life
        self.inputDict = inputDict
        self.outputVal = outputVal
        self.isInput = isInput
        self.isOutput = isOutput
        self.bias = bias
        self.immortal = self.isInput or self.isOutput
        
    def forward(self, step:int):
        if step <= 0:
            return 0
        output = 0
        for n in self.input_.keys():
            inp, coef = self.input_[n]
            output += inp.getOutput(step - 1) * coef
            
        return output
    
    def getOutput(self, step:int):
        if not self.isInput:
            self.outputVal = self.forward(step)
        return self.outputVal
    
    def setOutput(self, value:float):
        self.outputVal = value
        
    def addLink(self, inputNeural:object):
        self.inputDict[inputNeural] = [inputNeural, rg(0,1)]
        
    def deleteLink(self, inputNeural:object):
        self.inputDict.pop(inputNeural)
        
    def show(self, canvas, posX, posY, ray):
        self.canvas = canvas
        front_color = "green"
        back_color = "white"
        # si les deux sont faux créer un cercle blanc avec le pourcentage de vie en vert
         
        if self.isInput and not self.isOutput: # si input vrai et output faux créer un cercle bleu
            back_color = "blue"
        elif self.isOutput and not self.isInput: # si output vrai et input faux créer un cercle jaune
            back_color = "yellow"
        # si output vrai et input vrai créer un demi-cercle bleu et un demi-cercle jaune
        # Afficher le cercle
        self.canvas.create_oval(posX-ray, posY-ray, posX+ray, posY+ray, fill = back_color, width = max(1, ray//5))
        # Afficher la valeur du bias au centre
        
    def hurt(self, damage):
        #tester si non imortelle
            #Enlève de la vie
            # Kill si plus de vie
        pass
        
    def kill(self):
        #supprime le neurone
        #supprime ses connections dans le graph
        pass

# Création d'un objet Network graphique qui affiche le réseau
class Network():
    def __init__(self, canvas, input_nb, ouput_nb, start_nb, end_nb):
        self.canvas = canvas
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.input_nb = input_nb
        self.ouput_nb = ouput_nb
        self.start_nb = start_nb
        self.end_nb = end_nb
        self.inputList = [Perceptron(life = 100, isInput = True) for i in range(self.input_nb)]
        self.hiddenList = [Perceptron(life = 100) for i in range(self.end_nb)]
        self.outputList = [Perceptron(life = 100, isOutput = True) for i in range(self.ouput_nb)]
        
    def show(self):
        """ Affichage """
        # Afficher le neurone avec son niveau de vie et la valeur de son biais au milieu
        a = math.sin(math.pi/self.end_nb)
        PerceptSize = (self.height*a)/(1+a)
        # Afficher les inputs
        self.show_cols(space = PerceptSize, PerceptList = self.inputList, deltaX = PerceptSize)
        # Afficher le hidden layer en cercle
        self.show_cercle(space = PerceptSize, PerceptList = self.hiddenList, deltaX = 3*PerceptSize)
        # Afficher les outputs verticalement
        self.show_cols(space = PerceptSize, PerceptList = self.outputList, deltaX = 5*PerceptSize + self.height)
        # Afficher les connexions avec des pondérations
        
    def show_cols(self, space:float, PerceptList:list, deltaX:float):
        strat_pos = max(space//2, self.height/2-(space*(len(PerceptList)/2 - 0.5)))
        # Afficher les inputs verticalement à droite
        print(space, strat_pos)
        for i,n in enumerate(PerceptList):
            n.show(self.canvas, deltaX, strat_pos+i*space, int(space*0.40))
            
    def show_cercle(self, space:float, PerceptList:list, deltaX:float):
        for i,n in enumerate(PerceptList):
            h2 = self.height/2
            hyp = (h2-space)
            alpha2 = (2*math.pi/self.end_nb)*i
            n.show(self.canvas, deltaX + h2 + math.cos(alpha2) * hyp, h2 + math.sin(alpha2) * hyp, int(space*0.40))
       
    def train(self):
        """ Entrainement """
        # Loop Epoch
            # Loop Batch
                # parcourir le graph en un nombre limité de pas pour éviter des boucles infini
                # calcule de l'erreur
                # Modification des poids
                # soustraction du niveau de vie
            # Tuer les neurones sans vie
            # Reproduir les meilleurs selon le ratio (limite pop max)
            # Changer les connexions de manière aléatoire
            # Changer le graph avec la population
        pass

# Tool bar number input
class NumberInput(tk.Frame):
    def __init__(self, master, text:str, values:float = 0, from_:float = 0, to:float = None, slider:bool = False):
        #init parent
        self.master = master
        super().__init__(self.master, bd = 6)
        # init self variables
        self.text = text
        self.values = values
        self.from_ = from_
        self.to = to
        self.slider = slider
        self.nb_var = tk.DoubleVar()
        self.nb_var.set(self.values)
        #init graphique object
        self.text = tk.Label(self, text = self.text)
        self.text.pack(side = tk.TOP)
        if self.slider:
            #slider
            self.scale = tk.Scale(self, from_=0, to=1,resolution=0.001, length=180, orient = tk.HORIZONTAL, variable = self.nb_var).pack(side = tk.TOP)
        else:
            #spinbox
            self.spinbox = tk.Spinbox(self, values=self.values, from_=self.from_, to = self.to).pack(side = tk.TOP)
        #pack object in a master frame
        self.pack(side = tk.TOP)

#Creation d'objet graphique pour representer les connexions
class Ware(tk.Tk):
    ## Initialization ##
    def __init__(self):
        # Initialize the window
        super().__init__()
        # set window title
        self.title("Genetic Network Generator")
        # set window width and height
        self.geometry("1280x720")
        self.minsize(540,360)
        # set window background color
        self.configure(bg='white')
        #séparation de l'interface en 2 parties
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(expand=1, fill="both")
        # definir un canvas qui affiche le réseau
        self.canvas = tk.Canvas(self.mainFrame, bg = 'white')
        self.canvas.pack(side = tk.RIGHT, expand=1, fill="both")
        # Creat Tool frame
        self.tools = tk.Frame(self.mainFrame)
        self.tools.pack(side = tk.LEFT, fill=tk.Y)
        # Scroll Canvas
        self.ScrollCanvas = tk.Canvas(self.tools)
        self.ScrollCanvas.pack(side = tk.RIGHT, fill=tk.Y)
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tools, orient = tk.VERTICAL, command=self.ScrollCanvas.yview)
        self.scrollbar.pack(side = tk.LEFT, fill = tk.Y)
        # Configure the canvas
        self.ScrollCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.ScrollCanvas.bind('<Configure>', lambda e: self.ScrollCanvas.configure(scrollregion = self.ScrollCanvas.bbox("all")))
        # Tools bar
        self.toolsFrame = tk.Frame(self.ScrollCanvas)
        #Add that new frame to a window in the canvas
        self.ScrollCanvas.create_window((0,0), window = self.toolsFrame, anchor = "nw")
        #céation d'un module avec une image pour afficher l'évolution de la population
        self.text = tk.Label(self.toolsFrame, text = "Population size over time").pack(side = tk.TOP)
        self.figure = plt.Figure(figsize=(16,9), dpi=11)
        self.chart = FigureCanvasTkAgg(self.figure, self.toolsFrame)
        self.chart.get_tk_widget().pack()
        # définir une random seed
        self.pop_dep = NumberInput(self.toolsFrame, "Random Seed", values = 123)
        # définir la dataset
        self.dataset_text = tk.Label(self.toolsFrame, text = "Dataset").pack(side = tk.TOP)
        self.dataset_opts = [
        "MNIST"
        ]         
        self.dataset = tk.StringVar(self.toolsFrame)
        self.dataset.set(self.dataset_opts[0]) # default value
        self.DataDropDown = tk.OptionMenu(self.toolsFrame, self.dataset, *self.dataset_opts).pack(side = tk.TOP)
        # définir la population de départ
        self.pop_dep = NumberInput(self.toolsFrame, "Size of the\nstarting population", values = 10)
        # definir le nombre de tentative de création de connection dans le reseau de départ
        self.start_connection = NumberInput(self.toolsFrame, "number of connection\ncreation attempts per\nneuron at the starting\nnetwork (depends on\nthe creation probability)", values = 20)
        # définir le pourcentage de population
        self.pop = NumberInput(self.toolsFrame, "Population growth rate", values = 20)
        # definir la population max
        self.pop_max = NumberInput(self.toolsFrame, "Population Max", values = 100)
        # Nombre de pas dans le graph avant l'output
        self.step = NumberInput(self.toolsFrame, "Path size between\ninputs and outputs", values = 6)
        # définir le nombre d'époque d'entrainement
        self.epoch = NumberInput(self.toolsFrame, "Nuber of Epoch", values = 10)
        # définir la taille des batch
        self.batch = NumberInput(self.toolsFrame, "Batch size", values = 32)
        # Learning rate
        self.LR = NumberInput(self.toolsFrame, "Learning rate", values = 0.001)
        # definir la proba de la suppression d'une connexion
        self.drop = NumberInput(self.toolsFrame, "Probability of dropping\na connection", values = 0.3, slider = True)
        # definir la proba de la creation d'une connexion
        self.create = NumberInput(self.toolsFrame, "Probability of creating\na connection", values = 0.5, slider = True)
        #Création d'un boutton d'execution
        self.run_but = tk.Button(self.toolsFrame, text ="Run Network", command =lambda: self.run_train()).pack(side = tk.TOP)
        #main loop
        self.mainloop()
        
    def run_train(self):
        # Creation du réseau
        self.network = Network(canvas = self.canvas, input_nb = 30 , ouput_nb = 10, start_nb = 10, end_nb = 50)
        # Show Network
        self.network.show()
        # Entrainement
        self.network.train()

def main():
    """
    TO DO:
    limites des spinbox
    récupérer les valeurs dans la génération du model
    Affichage des neurones
    affichage des bias
    affichage de la vie
    affichage des liasons
    affichage des flèches
    affichage du coef
    
    création du graph
    transformer les graphs en arbres
    calcul forward
    calcul de l'erreur
    calcul du gradiant
    backpropagation
    suppression de sommet dans le graph
    ajout de sommet dans le graph
    ajout d'aretes dans le graph
    suppresion d'aretes dans le graph    
    
    forward en recursive terminal
    bug d'affichage sur la largeur de la tool bar
    traduidre les commentaires
    typer les input des fonctions
    Appliquer des docstring aux fonctions
    Créer un README
    
    Améliorations:
    Possibiliter de paramêtrer la fonction coût
    Proposer plusieurs méchanismes de reproduction
    Varier les méchanismes de création de suppression des connections
    Donner aux neurones la capacité de faire varier leur fonction interne
    Afficher le graph en 3D    
    """
    Ware()

if "__main__" == __name__:
    main()