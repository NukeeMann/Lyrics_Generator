# Rap Lyrics Generator
![Program](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/1.png)
## About the project
Purpose of this project is to generate rap lyrics based on songs provided and selected from the database. Since Hip-Hop, especially rap music is characterized by stong emotions, the occurrence of curses is possible. It would be pointless to edit delivered lyrics, beacuse they would lose their lyrical and artistic value.

## Database
The database consists of dozens of lyrcis grouped by artists in folders and one separate folder for lyrcis delivered by user.

![Database](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/2.png)

In every folder to every lyric there is assigned file with phonetic version of it.

![Lyrics](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/3.png)
![Phonetics](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/4.png)

## Creation of dictionaries
When files are loaded we are getting rid of all punctuation marks and brackets. Relevant indexes of words in normal and phonetic form are the same. Thanks to it we can assign 3 letter rhyme from phonetic version to every word. Next, from thoese words we are creating network that is based on Markov chains. Every word has a array with number of appearances of next, next after next, and the next after next after next word. The same goes with previous words.
On an example:

>#### _`I promise t never go back on that promise`_

After processing word `back` our program will deploy words around it in arrays (or increase number of appearance) in such a way.

![Markov_1](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/5.png)

When our program will finish processing all words in our sentence we will recive specified network of connections.

![Markov_2](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/6.png)

As we can see we are getting compacted network which will give us wide range of possibilities when creating our algorithm.

## Data storage
Besides dictionaries of words with their connections we are creating seperate dictionary with rhyming words. For example, in one group we will store all words ending with `ing`. After processing every word from chosen lyrics from database, we are calculating probability of occurrence of every word after another by dividing the number of occurrence by amount of all words in particular list. We receive two dictionaries - of words and rhymes.

## Algorithm #1
Based on assumptions above, two algorithms were developed. First one is characterized by more frequent appearance of rhymes inside the sentence but less logic.

It works as follows.
- At the beginning in every verse we draw rhyme from rhyme dictionary. This will determine how two sentences will rhyme.
- We are generating words in one line as long as we meet a word that fit with our rhyme.
  1. If in the array of next words after the last one added to line is word that rhymes with our chosen rhyme - we take it.
  2. If in the array of next words of any next word is our rhyme (that means that the next word we take will met our 1st condition) - we take it.
  3. The same thing but one more step further.
  4. If listed methods fail we count probability of occurrence of the next word by adding values from next_word array and increasing them if there is connection with previous word (Thanks to that our sentence will make more sense) and we take the first word that will pass 0.5
 - If amount of words in single line exceeds 10 and we still don't have word that will have our chosen rhyme, we generate it by picking one of the words under our category from rhyme dictionary.
 
 #### Examples:
 
![Algorithm_1_1](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/11.png)
![Algorithm_1_2](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/12.png)
![Algorithm_1_3](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/13.png)
![Algorithm_1_4](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/14.png)
![Algorithm_1_5](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/15.png)
![Algorithm_1_6](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/16.png)
![Algorithm_1_7](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/17.png)

As we can see there are forming many inaccurate rhymes. Generated lines doesn't allways make sense but are not copied 1 to 1 from original lyrics from database.

## Algorithm #2
In the second algorithm we focused on that the generated lines will make more sense. Consequently, the amount of rhyme decreased. We don't chose rhyme befor the line even begins. Instead when the first of two line reaches 10 words we take the last one and we impose the rhyme only to second line so that it will fit with the 10th word.

Proccess of generating words works as follows:
- We take 3 last added words _prev_prev_word_, _prev_word_, and _word_ .
- We take words from the _next_word_ array and count their probability by adding values from arrays _next_word_ from _word_, _next_next_word_ from _prev_word_ and _next_next_next_word_ from _prev_prev_word_ . 
Illustration for visualization

![Algorithm_2_0](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/20.png)
- Next, from list of possible next words we multiply valuse of words that have our rhyme by 1.2 and we choose the two largest.
- In the last step we draw a number from zero to one and if it is bigger than 0.3 we take the word that has bigger value. Otherwise we take the lower one.

#### Examples

![Algorithm_2_1](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/21.png)
![Algorithm_2_2](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/22.png)
![Algorithm_2_3](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/23.png)
![Algorithm_2_4](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/24.png)
![Algorithm_2_5](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/25.png)
![Algorithm_2_6](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/26.png)
![Algorithm_2_7](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/27.png)
![Algorithm_2_8](https://github.com/NukeeMann/Lyrics_Generator/blob/master/img_readme/28.png)

As we can see generated lines make more sense and form more logical sentences. The number of rhyme has decreased
