## conversation initialization
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_start_conversation



## story path - first time conversation happy path continue
* user.first_time
  - request_sport
  - form{"name": "request_sport"}
  - form{"name": null}
  - utter_ask_continue
* affirm
  - request_sport
  - form{"name": "request_sport"}
  - form{"name": null}



## story path - first time conversation happy path discontinue
* user.first_time
  - request_sport
  - form{"name": "request_sport"}
  - form{"name": null}
  - utter_ask_continue
* deny
  - utter_greet.bye



## story path - first time conversation generated
* user.first_time
  - request_sport
  - form{"name": "request_sport"}
  - slot{"requested_slot": "type_of_topic"}
* form: inform{"type_of_topic": "basketball"}
  - form: request_sport
  - slot{"type_of_topic": "basketball"}
  - slot{"requested_slot": "reason_of_like"}
* form: inform{"reason_of_like": "fun"}
  - form: request_sport
  - slot{"reason_of_like": "fun"}
  - slot{"requested_slot": "recent_active"}
* form: inform{"recent_active": True} OR affirm
  - form: request_sport
  - slot{"recent_active": "True"}
  - form{"name": null}



## story path - first time conversation user reject
* user.first_time
  - request_sport
  - form{"name": "request_sport"}
* deny OR user.reject 
  - utter_reply.to.reject
  - action_deactivate_form
  - form{"name": null}



## story path - second time conversation
* user.second_time
  - inquire_sport

<!---------------------------->
<!-- generic conversations  -->
<!---------------------------->


## story - thank
* user.thank
  - utter_reply.to_thank

## story - sad
* user.sad
  - utter_reply.to_sad

## story - good
* user.good
  - utter_reply.to_good

## story - bye
* user.bye  
  - utter_temp

## story - affirm deny
* affirm OR deny
  - utter_thumbsup

## story - affirm v2
* affirm 
  - utter_great
  

<!---------------------------->
<!--     out of scope       -->
<!---------------------------->


## out of scope - non english
* out.of.scope.non.english
  - utter_reply.to_out_of_scope_non_english
    
## out of scope - other
* out.of.scope.other
  - utter_reply.to_out_of_scope_other

## bot challenge
* bot_challenge
  - utter_iamabot

## user reject
* user.reject
  - utter_reply.to.reject