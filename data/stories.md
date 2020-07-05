## story - default
* user.hello
  - action_greet
  - slot{"greeted":true}
* chit_chat OR chit_chat_non_english OR enter_data OR user.hello
  - set_name


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
    - slot{"email":"sheep42@google.com"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - action_take_path
    - set_name
    - form{"name":"set_name"}
    - slot{"requested_slot":"person"}
* enter_data
    - set_name
    - slot{"person":"my name shrek"}
    - slot{"person":"shrek"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - request_fav_sport
    - form{"name":"request_fav_sport"}
    - slot{"requested_slot":"type_of_sport"}
* enter_data{"sport":"swimming"}
    - request_fav_sport
    - slot{"type_of_sport":"swimming"}
    - slot{"type_of_sport":"swimming"}
    - form{"name":null}
    - slot{"requested_slot":null}
* affirm OR deny OR enter_data OR user.bye OR chit_chat_question OR chit_chat
    - action_custom_listen
    - request_fav_sport_reason
    - form{"name":"request_fav_sport_reason"}
    - slot{"requested_slot":"reason_of_like_sport"}
* chit_chat
    - request_fav_sport_reason
    - slot{"reason_of_like_sport":"because it's very fun"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - request_fav_animal
    - form{"name":"request_fav_animal"}
    - slot{"requested_slot":"type_of_animal"}
* enter_data{"animal":"dog"}
    - request_fav_animal
    - slot{"type_of_animal":"dog"}
    - slot{"type_of_animal":"dog"}
    - form{"name":null}
    - slot{"requested_slot":null}
* affirm OR deny OR enter_data OR user.bye OR chit_chat_question OR chit_chat
    - action_custom_listen
    - action_store_detail