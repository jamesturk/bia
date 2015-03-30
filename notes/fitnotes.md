# Core

Category
    _id
    name

exercise
    _id
    name
    category_id
    exercise_type_id
    notes
    weight_increment

# Log

training_log
    _id
    exercise_id
    date
    metric_weight
    reps
    unit
    routine_section_exercise_set_id
    timer_auto_start
    is_personal_record
    is_personal_record_first
    is_complete

# Routines

Routine
    _id
    name
    notes

RoutineSection
    _id
    routine_id
    name
    sort_order

RoutineSectionExercise
    _id
    routine_section_id
    exercise_id
    sort_order

RoutineSectionExerciseSet
    _id
    routine_section_exercise_id
    metric_weight
    reps
    sort_order

WorkoutGroup
    _id
    name
    date
    colour
    routine_section_id

WorkoutGroupExercise
    _id
    exercise_id
    date
    routine_section_id
    workout_group_id

# Other

BodyWeight
    _id
    date
    body_weight_metric
    body_fat
    comments

Goal
   _id
   type_id
   exercise_id
   metric_weight
   reps
   unit
   title
   target_date
   sort_order

ExerciseGraphFavourite
    _id
    group_id
    exercise_id
    graph_type_id
    time_period
    sort_order

Comment
    _id
    date
    owner_type_id       # used as a generic foreign key construct
    owner_id
    comment

# FitNotes specific

android_metadata
    locale

settings
    _id
    metric
    navigation_position
    weight_increment
    body_weight_increment
    body_weight_goal
    body_weight_goal_weight
    body_weight_show_in_workout_log
    estimated_1rm_max_reps_to_include
    estimated_1rm_max_apply_to_graph
    track_personal_records
    mark_sets_complete
