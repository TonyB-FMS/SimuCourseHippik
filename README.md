# Simulateur de course hippique

### Exercice

Une course de trot attelé2 rassemble 12 à 20 chevaux, chacun tractant un sulky,
et étant mené par un driver.Elle peut faire l’objet d’un tiercé, d’un quarté, ou d’un quinté. 

La course est supposée se dérouler sur un hippodrome rectiligne (chaque cheval 
disposant de son propre couloir), d’une longueur de 2 400 m.

Il est à noter que chaque cheval doit respecter l’allure du trot de bout en bout, 
le passage au galop entrainant sa disqualification. 


L’utilisateur saisit au démarrage le nombre de chevaux et le type de la course.

La course se déroule à la manière d’un « jeu de plateau » : à chaque tour de jeu, 
chaque cheval fait l’objet d’un jet de dé (à 6 faces), qui décide d’une altération 
possible de sa vitesse (augmentation, stabilisation, diminution). 
La nouvelle vitesse détermine alors la distance dont il avance. 

Chaque tour de jeu représente 10 secondes du déroulement de la course, 
mais le temps ne sera pas rendu dans le programme. C’est l’utilisateur qui fera 
avancer la course de tour en tour, à la suite d’un message du programme l’y invitant.

Le tableau suivant indique les évolutions de la vitesse d’un cheval, 
selon sa vitesse actuelle, et le jet d’un dé (DQ indique que le cheval est disqualifié).

![Capture d’écran 2024-07-19 141439](https://github.com/user-attachments/assets/7762e3a6-2e47-49c5-8971-c718e52f7177)

Le tableau qui suit donne pour sa part la distance dont avance un cheval lors d’un tour 
de jeu suivant sa vitesse.

![Capture d’écran 2024-07-19 141642](https://github.com/user-attachments/assets/47fa81c3-454c-4b1a-aca1-1b29eaded908)

Chaque cheval démarre la course à l’arrêt. Lors de chaque tour, chaque cheval voit 
sa vitesse évoluer, puis parcourir la distance correspondant à sa nouvelle vitesse. 
Il peut être intéressant d’afficher alors le temps écoulé, la vitesse et la distance 
parcourue par chaque cheval. 

La course se déroule jusqu’à ce que le dernier cheval 
non disqualifié ait franchit la ligne d’arrivée. On n’affichera cependant que 
les 3, 4 ou 5 premiers chevaux arrivés (suivant le type de la course).

Optionnel : afficher après chaque tour une progression visuelle de chaque cheval vis-à-vis de la 
ligne d’arrivée.
