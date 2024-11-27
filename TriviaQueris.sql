--Queries for the trivia project

--Trivia questions insertion and improves

INSERT INTO questions (question_text, answer_a, answer_b, answer_c, answer_d, correct_answer) VALUES
('What is the largest planet in our solar system?', 'Earth', 'Jupiter', 'Saturn', 'Neptune', 'b'),
('Who wrote "To Kill a Mockingbird"?', 'J.K. Rowling', 'F. Scott Fitzgerald', 'Harper Lee', 'Ernest Hemingway', 'c'),
('What is the capital of Japan?', 'Tokyo', 'Beijing', 'Seoul', 'Bangkok', 'a'),
('In which year did World War II end?', '1939', '1941', '1943', '1945', 'd'),
('What is the chemical symbol for water?', 'H2O', 'CO2', 'NaCl', 'O2', 'a'),
('Who painted the Mona Lisa?', 'Pablo Picasso', 'Michelangelo', 'Leonardo da Vinci', 'Vincent van Gogh', 'c'),
('How many continents are there?', '5', '6', '7', '8', 'c'),
('What is the powerhouse of the cell?', 'Nucleus', 'Mitochondria', 'Ribosome', 'Cytoplasm', 'b'),
('Which planet is known as the Red Planet?', 'Venus', 'Jupiter', 'Mars', 'Saturn', 'c'),
('Who discovered penicillin?', 'Alexander Fleming', 'Marie Curie', 'Thomas Edison', 'Albert Einstein', 'a'),
('What is the capital of Canada?', 'Toronto', 'Vancouver', 'Ottawa', 'Montreal', 'c'),
('Which organ pumps blood throughout the human body?', 'Brain', 'Lungs', 'Kidney', 'Heart', 'd'),
('What is the largest mammal in the world?', 'Elephant', 'Great White Shark', 'Blue Whale', 'Giraffe', 'c'),
('Who was the first person to walk on the moon?', 'Yuri Gagarin', 'Neil Armstrong', 'Buzz Aldrin', 'Alan Shepard', 'b'),
('What is the freezing point of water in Celsius?', '100', '32', '0', '-10', 'c'),
('What does “www” stand for in a website browser?', 'World Web Wide', 'World Wide Web', 'Web Wide World', 'Web World Wide', 'b'),
('Which country gifted the Statue of Liberty to the United States?', 'Germany', 'Italy', 'France', 'Spain', 'c'),
('How many colors are in a rainbow?', '5', '6', '7', '8', 'c'),
('Who invented the telephone?', 'Thomas Edison', 'Alexander Graham Bell', 'Nikola Tesla', 'Albert Einstein', 'b'),
('What is the tallest mountain in the world?', 'K2', 'Kangchenjunga', 'Mount Everest', 'Mount Kilimanjaro', 'c');
UPDATE questions SET question_text = 'Which city in Japan was the first to host the Summer Olympics?', answer_a = 'Kyoto', answer_b = 'Osaka', answer_c = 'Tokyo', answer_d = 'Sapporo', correct_answer = 'c' WHERE question_text = 'What is the capital of Japan?';

UPDATE questions SET question_text = 'Which novel by George Orwell features the concept of ''Big Brother''?', answer_a = 'Animal Farm', answer_b = 'Nineteen Eighty-Four', answer_c = 'Homage to Catalonia', answer_d = 'The Road to Wigan Pier', correct_answer = 'b' WHERE question_text = 'Who wrote "To Kill a Mockingbird"?';

UPDATE questions SET question_text = 'What is the chemical symbol for table salt?', answer_a = 'H2O', answer_b = 'NaCl', answer_c = 'KCl', answer_d = 'CO2', correct_answer = 'b' WHERE question_text = 'What is the chemical symbol for water?';

UPDATE questions SET question_text = 'Who discovered radium?', answer_a = 'Alexander Fleming', answer_b = 'Albert Einstein', answer_c = 'Marie Curie', answer_d = 'Thomas Edison', correct_answer = 'c' WHERE question_text = 'Who discovered penicillin?';

UPDATE questions SET question_text = 'Which mammal has the longest gestation period?', answer_a = 'African Elephant', answer_b = 'Blue Whale', answer_c = 'Giraffe', answer_d = 'Rhinoceros', correct_answer = 'a' WHERE question_text = 'What is the largest mammal in the world?';

UPDATE questions SET question_text = 'Which planet has the strongest magnetic field in our solar system?', answer_a = 'Earth', answer_b = 'Saturn', answer_c = 'Jupiter', answer_d = 'Neptune', correct_answer = 'c' WHERE question_text = 'What is the largest planet in our solar system?';

UPDATE questions SET question_text = 'Which continent has the highest number of countries?', answer_a = 'Asia', answer_b = 'Africa', answer_c = 'Europe', answer_d = 'North America', correct_answer = 'b' WHERE question_text = 'How many continents are there?';

UPDATE questions SET question_text = 'Which planet has the tallest volcano in the solar system?', answer_a = 'Venus', answer_b = 'Earth', answer_c = 'Mars', answer_d = 'Jupiter', correct_answer = 'c' WHERE question_text = 'Which planet is known as the Red Planet?';

UPDATE questions SET question_text = 'Which mission was the first to orbit the moon and send back photos of its surface?', answer_a = 'Apollo 11', answer_b = 'Apollo 8', answer_c = 'Luna 3', answer_d = 'Mariner 2', correct_answer = 'b' WHERE question_text = 'Who was the first person to walk on the moon?';

UPDATE questions SET question_text = 'What organelle is primarily responsible for photosynthesis in plant cells?', answer_a = 'Chloroplast', answer_b = 'Nucleus', answer_c = 'Mitochondria', answer_d = 'Ribosome', correct_answer = 'a' WHERE question_text = 'What is the powerhouse of the cell?';



--Players and admin INSERT

insert into players (username, "password", email, age) values ('Administrator', 'admin', 'admin@gmail.com', 22)
INSERT INTO players (username, "password", email, age) VALUES
('User1', 'password123', 'user1@example.com', 21),
('User2', 'securepass', 'user2@example.com', 25),
('User3', 'mypassword', 'user3@example.com', 19),
('User4', 'pass1234', 'user4@example.com', 28),
('User5', 'qwerty789', 'user5@example.com', 23),
('User6', 'letmein456', 'user6@example.com', 30),
('User7', 'password567', 'user7@example.com', 26),
('User8', 'abc123xyz', 'user8@example.com', 24),
('User9', 'zxcvbn123', 'user9@example.com', 22),
('User10', 'unique1234', 'user10@example.com', 20);



--checkUsername FUNCTION

create or replace function checkUsername(_username text)
--If the username exists, it return TRUE, otherwise FALSE
returns bool 
language plpgsql as $$
DECLARE
	userExists text;
begin 
	select username into userExists from players where username = _username;
	if userExists is not null then 
		return true ;
	else 
		return false ;
end if;		
end;
$$;



--checkEmail FUNCTION

create or replace function checkEmail(_email text)
--If the email exists, it return TRUE, otherwise FALSE
returns bool 
language plpgsql as $$
DECLARE
	emailExists text;
begin 
	select email into emailExists from players where email = _email;
	if emailExists is not null then 
		return true ;
	else 
		return false ;
end if;		
end;
$$;


--addUser function

create or replace procedure addUser(_username text, _email text, _age int, _password text)
--Adds a new user (SignUp)
language plpgsql as $$
begin 
	insert into players (username, email, age, password) values (_username, _email, _age, _password);
end;
$$;


--This function shows how many players played
create or replace function players_played()
returns int as $$	
declare
	total int := 0;
begin 
	select count(*) into total from players where questions_solved > 0;		
	return total;
end;
$$ language plpgsql;



--Login function
create or replace function user_login(_username text, _password text)
returns int as $$
begin
	if (select password from players where username = _username) = _password then
		return (select player_id from players where username = _username);
	else
		return 0;
	end if;
end;
$$ language plpgsql;


--This function returns the id of questions that have been answered by id
create or replace function answered_questions(_id int)
returns int[] as $$
declare 
	i int:= 0;
	answered int[];
begin 	
	select array(select question_id from player_answers where player_id = _id)
	into answered;
	return answered;
end;
$$ language plpgsql;


--This function returns the amount of correct and incorrect answeres in an array
create or replace function answers_amount(_id int)
returns int [] as $$
declare 
	answered int[] := ARRAY[0, 0];  
    correct_count int;
    incorrect_count int;
begin
	select count(*) into correct_count from player_answers where player_id = _id and is_correct = true;
	select count(*) into incorrect_count from player_answers where player_id = _id and is_correct = false;
	
    answered[1] := correct_count;
	answered[2] := incorrect_count;

	return answered;
end;
$$ language plpgsql;


--Bonus function and trigger, updates solved_questions
create or replace function update_questions_solved()
returns trigger as $$
begin 
	update players 
	set questions_solved = (select count(*) from player_answers where player_id = new.player_id)
	where player_id = new.player_id;
	
	return new;
end;
$$ language plpgsql;

create trigger trigger_update_questions_solved
after insert on player_answers
for each row 
execute function update_questions_solved();


--This function reset the players question_solved in both tables
create or replace procedure reset_solved(_id int)
language plpgsql
as $$
begin 
	delete from player_answers where player_id = _id;
	update players set questions_solved = 0 where player_id = _id;
end;
$$;


--This function returns the ids of the question that most players answered correctly
create or replace function easiest_question()
returns int[] as $$
declare 
	ans int[] = '{}';
begin 
	select ARRAY_AGG(question_id) into ans from (
	select question_id from questions q 
	join player_answers pa using (question_id)
	group by question_id having count(is_correct) =  
	(select count(is_correct) from questions q 
	join player_answers pa using (question_id) 
	group by question_id order by count desc limit 1));

	return ans;


end;
$$ language plpgsql;


--This function returns the ids of the question that least players answered correctly
create or replace function hardest_question()
returns int[] as $$
declare 
	ans int[] = '{}';
begin 
	select ARRAY_AGG(question_id) into ans from (
	select question_id from questions q 
	join player_answers pa using (question_id)
	group by question_id having count(is_correct) =  
	(select count(is_correct) from questions q 
	join player_answers pa using (question_id) 
	group by question_id order by count limit 1));

	return ans;


end;
$$ language plpgsql;

--This view displays the players that answered most questions correctly in descending order
create or replace view most_answered_correctly_view as 
select username, count(is_correct) from players join player_answers pa using (player_id)
where is_correct = true group by username order by count desc;



--This view displays the players that answered most questions in descending order
create or replace view most_answered_totally_view as 
select username, questions_solved from players order by questions_solved DESC;


--Bonus, this view displays each question stats
create or replace view question_stats as
with total_answers as (
    select question_id, question_text, count(*) as total
    from questions
    join player_answers pa using (question_id)
    group by question_id, question_text
),
correct_answers as (
    select question_id, count(*) as correct
    from questions
    join player_answers pa using (question_id)
    where is_correct = true
    group by question_id
),
incorrect_answers as (
    select question_id, count(*) as incorrect
    from questions
    join player_answers pa using (question_id)
    where is_correct = false
    group by question_id
)
select 
    t.question_text,
    t.total,
    c.correct as correct,
    i.incorrect as incorrect
from total_answers t
left join correct_answers c on t.question_id = c.question_id
left join incorrect_answers i on t.question_id = i.question_id;

--Bonus matplotlib pie chart function that return in an array the values of the pie
create or replace function question_pie(_id int)
returns int[] as $$
declare 
	ans int[] := ARRAY[0, 0, 0];
	unanswered int := 20;
	correct int := 0;
	incorrect int := 0;
begin
	select count(*) into unanswered from player_answers where player_id = _id;
	select count(*) into correct from player_answers where player_id = _id and is_correct = true; 
	select count(*) into incorrect from player_answers where player_id = _id and is_correct = false;
	ans[1] := unanswered;
	ans[2] := correct;
	ans[3] := incorrect;
	return ans;
end;
$$ language plpgsql;