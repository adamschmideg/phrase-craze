-- Create Questions table
CREATE TABLE public.questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    text TEXT NOT NULL,
    difficulty INTEGER NOT NULL DEFAULT 1
);

-- Create Answers table
CREATE TABLE public.answers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    question_id UUID NOT NULL REFERENCES public.questions(id),
    text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    difficulty INTEGER NOT NULL DEFAULT 1
);

-- Create Status table
CREATE TABLE public.status (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL,
    question_difficulty INTEGER NOT NULL,
    answer_difficulty INTEGER NOT NULL,
    match_in_round_index INTEGER NOT NULL
);

-- Add indexes for better query performance
CREATE INDEX idx_answers_question_id ON public.answers(question_id);
CREATE INDEX idx_status_user_id ON public.status(user_id);
