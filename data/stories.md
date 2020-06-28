## story - default
* user.hello
  - action_greet
  - slot{"greeted":true}
* chit_chat OR chit_chat_non_english OR enter_data OR user.hello
  - action_set_name


## story - default 1
* affirm
  - action_get_answer

## story - default 2
* user.thank
  - action_get_answer

## story - default 3
* user.sad
  - action_get_answer

## story - default 4
* user.good
  - action_get_answer

## story - default 5
* user.bye  
  - utter_greet.bye

## story - default 7
* nice_to_meet_you
  - utter_reply.to_nice_to_meet_you

## story - default 8
* enter_data
  - utter_acknowledge
  - action_self_disclosure

## story - default 9
* user.reject
  - utter_reply.to.reject
  - utter_greet.bye



## chit chat 1
* chit_chat_non_english
  - utter_only_english
    
## chit chat 2
* chit_chat
  - action_get_answer

## chit chat 3
* chit_chat_question
  - action_get_answer

## chit chat 4
* bot_challenge
  - action_get_answer




## generated 1
* user.hello
  - action_greet
  - slot{"greeted":true}
  - request_email
  - form{"name":"request_email"}
  - slot{"requested_slot":"email"}
* enter_data
  - request_email
  - slot{"email":"sheep10@google.com"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - action_take_path
* chit_chat_question{"PERSON":"david"} OR chit_chat{"PERSON":"david"} OR chit_chat_non_english{"PERSON":"david"} OR enter_data{"PERSON":"david"} OR user.bye{"PERSON":"david"} OR user.hello{"PERSON":"david"}
  - action_set_name
  - slot{"PERSON":"david"}
  - action_process_name
  - request_fav_sport
  - form{"name":"request_fav_sport"}
  - slot{"requested_slot":"type_of_sport"}
* enter_data{"sport":"swimming"}
  - request_fav_sport
  - slot{"type_of_sport":"swimming"}
  - form{"name":null}
  - slot{"requested_slot":null}
* affirm OR chit_chat OR chit_chat_question OR enter_data
  - action_add_on_1
  - request_fav_sport_reason
  - form{"name":"request_fav_sport_reason"}
  - slot{"requested_slot":"reason_of_like_sport"}
* chit_chat OR affirm
  - request_fav_sport_reason
  - slot{"reason_of_like_sport":"because it's a good exercise and you can't sweat because you are in water"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - request_fav_animal
  - form{"name":"request_fav_animal"}
  - slot{"requested_slot":"type_of_animal"}
* enter_data{"animal":"pig"} OR affirm{"animal":"pig"}
  - request_fav_animal
  - slot{"type_of_animal":"pig"}
  - form{"name":null}
  - slot{"requested_slot":null}
* chit_chat_question OR affirm OR chit_chat
  - action_add_on_2
  - action_store_detail
  - slot{"type_of_sport":null}
  - slot{"reason_of_like_sport":null}
  - slot{"recent_active_sport":null}
  - slot{"type_of_animal":null}
  - slot{"own_animal":null}
  - slot{"animal_breed":null}
  - slot{"plan_to_own_animal":null}
  - action_end_session_1


## generated 2
* user.hello
  - action_greet
  - slot{"greeted":true}
  - request_email
  - form{"name":"request_email"}
  - slot{"requested_slot":"email"}
* enter_data
  - request_email
  - slot{"email":"sheep33@google.com"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - action_take_path
* enter_data
  - action_set_name
  - slot{"PERSON":"zero"}
  - action_process_name
  - request_fav_sport
  - form{"name":"request_fav_sport"}
  - slot{"requested_slot":"type_of_sport"}
* enter_data{"sport":"swimming"}
  - request_fav_sport
  - slot{"type_of_sport":"swimming"}
  - form{"name":null}
  - slot{"requested_slot":null}
* enter_data{"sport":"soccer"}
  - action_add_on_1
  - request_fav_sport_reason
  - form{"name":"request_fav_sport_reason"}
  - slot{"requested_slot":"reason_of_like_sport"}



## generated 3
* user.hello
    - action_greet
    - slot{"greeted":true}
    - request_email
    - form{"name":"request_email"}
    - slot{"requested_slot":"email"}
* enter_data
    - request_email
    - slot{"email":"sheep23@google.com"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - action_take_path
* chit_chat OR chit_chat_non_english OR enter_data OR user.hello
    - action_set_name
