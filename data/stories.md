## story - user first time, recent active true
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
* enter_data
  - request_detail
  - form{"name": "request_detail"}
  - form{"name": null}
  - request_more_detail
  - form{"name": "request_more_detail"}
  - slot{"requested_slot": "recent_active"}
* form: affirm
  - form: request_more_detail
  - slot{"recent_active": true}
  - form{"name": null}
  - action_store_detail
  - action_ask_continue



## story - user first time, own animal false
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
* enter_data
  - request_detail
  - form{"name": "request_detail"}
  - form{"name": null}
  - request_more_detail
  - form{"name": "request_more_detail"}
  - slot{"requested_slot": "own_animal"}
* form: deny
  - form: request_more_detail
  - slot{"own_animal": false}
  - form{"name": null}
  - action_store_detail
  - action_ask_continue


## story - user first time and continue
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
  - action_opening_question
* enter_data
  - request_detail
  - form{"name": "request_detail"}
  - form{"name": null}
  - request_more_detail
  - form{"name": "request_more_detail"}
  - form{"name": null}
  - action_store_detail
  - action_ask_continue
* affirm
  - action_more_topic
* enter_data
  - action_more_topic_process



## story - user first time and discontinue
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
* enter_data
  - request_detail
  - form{"name": "request_detail"}
  - form{"name": null}
  - request_more_detail
  - form{"name": "request_more_detail"}
  - form{"name": null}
  - action_store_detail
  - action_ask_continue
* deny
  - utter_greet.bye



## story - user refuse give email
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
* user.reject OR deny OR out.of.scope.other
  - utter_reply.to.reject
  - utter_greet.bye
  - action_deactivate_form
  - form{"name": null}



## story - user has no interest
* user.hello
  - utter_greet.hi
  - request_email
  - form{"name": "request_email"}
  - form{"name": null}
  - action_take_path
* enter_data
  - request_detail
  - form{"name": "request_detail"}
  - slot{"requested_slot": "type_of_topic"}
* user.reject OR deny OR out.of.scope.other
  - utter_reply.to.reject
  - utter_greet.bye
  - action_deactivate_form
  - form{"name": null}


## story - user wants more topics
* wants_to_talk OR enter_data
  - request_detail
  - form{"name": "request_detail"}
  - form{"name": null}

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

## story - user ask question
* user.question
  - utter_reply.to_questions

## story - user ask how doing
* ask_howdoing
  - utter_reply.to_howdoing

## story - user insult
* user.insult
  - utter_reply.to_insult

## story - user nice to meet you
* nicetomeeyou
  - utter_reply.to_nicetomeetyou



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
  - utter_greet.bye