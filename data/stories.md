## story - user first time
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path


## story - user continues
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
  - request_detail
  - form{"name": "request_detail"}
  - slot{"requested_slot": "recent_active"}
* form: inform{"recent_active": True} OR affirm
  - form: request_detail
  - slot{"recent_active": "True"}
  - form{"name": null}
  - action_store_detail
  - utter_ask_continue
* affirm 
  - action_more_topic
* enter_data OR out.of.scope.other OR out.of.scope.non.english
  - action_more_topic_process


## story - user refuse give email
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
* user.reject OR deny
  - form{"name": null}
  - utter_greet.bye


## story - user has no interest
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
  - request_detail
  - form{"name": "request_detail"}
  - slot{"requested_slot": "type_of_topic"}
* user.reject OR deny
  - slot{"type_of_topic": "None"}
  - form{"name": null}
  - utter_greet.bye


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
  - utter_greet.bye

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