## Task Description
Please create a web application in python using pyramid framework which has one endpoint /benford that accepts a csv file with just one column with 10k+ rows of numbers as input. Please produce a json output if the input csv conforms the Benford’s law on first digits.

### User Input 
- CSV file for the dataset that will have one column with 10k+ rows of number

### Features of web app
1. An endpoint /benford to accept user's input
2. Check if input CSV file conforms Benford's law on first digits
3. Return json output if the input csv conforms the Benford's law

### Technology to be used
- Python
- Pyramid

### About Benford's law
 - In any dataset if we take the first digit of all the rows, the most frequenct 1st digit will be 1 and the frequency decreases gradually. The weird thing is that it is correct for almost all the naturally occuring data.
- Benford’s law describes the relative frequency distribution for leading digits of numbers in datasets. Leading digits with smaller values occur more frequently than larger values. This law states that approximately 30% of numbers start with a 1 while less than 5% start with a 9. According to this law, leading 1s appear 6.5 times as often as leading 9s! Benford’s law is also known as the First Digit Law.
![Bendford data distribution](https://i0.wp.com/statisticsbyjim.com/wp-content/uploads/2022/10/Benfords_law_frequencies.png?w=461&ssl=1)
 - However it may not work for height data, CGPA data etc.
 - Check this [YT Video](https://www.youtube.com/watch?v=oH1ZF0OOf-c)
 - And this [Blog](https://statisticsbyjim.com/probability/benfords-law/)
 - Used mostly in digital forensics, anomaly detection, fraud detection