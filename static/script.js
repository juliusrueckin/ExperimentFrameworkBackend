var i = 0;

$(document).ready(function(){
	/*$("#params_fields").html(
		'<span style="margin: 25px 0px; border-bottom: 1px solid lightgray; display: block;"><span class="input_field"><label for="name_' + i + '">Parameter name</label><input type="text" name="params[' + i + '][name]" id="name_' + i + '" placeholder="Type in parameter name, such as threshold"></span><span class="input_field"><label for="value_' + i + '">Parameter value</label><input type="text" name="params[' + i + '][value]" id="value_' + i + '" placeholder="Type in parameter value, such aus 0.5"></span></span>'
	);*/
	isOfTypeStringArr = {};

	$("body").delegate(".valueDataTypeCheckbox", "click", function(){
		isOfTypeStringArr[$(this).attr("id")] = !isOfTypeStringArr[$(this).attr("id")];
	});

	$("body").delegate("#add_param_field_button", "click", function(){
		isOfTypeStringArr["value_"+i+"_dataTypeOfValue"] = true;
		current_fields = $("#params_fields").html();
		$("#params_fields").html(current_fields + 
		'<span class="param_pair" style="margin: 25px 0px; border-bottom: 1px solid lightgray; display: block;"><span class="input_field"><label for="name_' + i + '">Parameter name</label><input type="text" name="params[' + i + '][name]" data-param-index="' + i + '" id="name_' + i + '" placeholder="Type in parameter name, such as threshold"></span><span class="input_field"><label for="value_' + i + '">Parameter value</label><input type="text" name="params[' + i + '][value]" data-param-index="' + i + '" class="param_value_input_field" id="value_' + i + '" placeholder="Type in parameter value, such aus 0.5"><span class="valueDataTypeCheckboxWrapper"><input class="valueDataTypeCheckbox" type="checkbox" id="value_'+i+'_dataTypeOfValue" value="isString" checked><label for="value_'+i+'_dataTypeOfValue">is String?</label></span></span></span>'); 
		i += 1;
	});

	$("#createConfigForm").on("submit", function(e){
		e.preventDefault();
		e.stopPropagation();

		conf = {"params": []};
		formArray = $(this).serializeArray();
		p = 0;
		for (var j = 0; j < formArray.length; j++){
			if(!formArray[j]['name'].includes('params'))
				conf[formArray[j]['name']] = formArray[j]['value'];
			else{
				if(formArray[j]['name'].includes('name')){
					k = j + 1;
					paramStr = '{"name": "'+formArray[j]["value"]+'", "value": '+formArray[k]["value"]+'}';
					if(isOfTypeStringArr["value_"+p+"_dataTypeOfValue"]){
						paramStr = '{"name": "'+formArray[j]["value"]+'", "value": "'+formArray[k]["value"]+'"}';
					}
					conf.params.push(JSON.parse(paramStr));
					p += 1;
				}
			}
		}

		conf.csvFields = conf.csvFields.split(",");

		extractTimeoutProperties(conf);
		extractSlackNotifier(conf);
		extractTelegramNotifier(conf);
		extractMailNotifier(conf);

		$.post("/createFiles",{basicConfObj: JSON.stringify(conf), timeoutConfObj: JSON.stringify(timeoutConf), slackNotifierConfObj: JSON.stringify(slackNotifierConf), mailNotifierConfObj: JSON.stringify(mailNotifierConf), telegramNotifierConfObj: JSON.stringify(telegramNotifierConf)},function(data){
			alert(data);
		});
	});
});

function extractTimeoutProperties(conf){
	timeoutConf = {};

	timeoutConf['defaultTimeout'] = parseInt(conf.defaultTimeout);
	delete conf.defaultTimeout;

	timeoutConf['outputPattern'] = conf.outputPattern;
	delete conf.outputPattern;

	timeoutConf['maxTimeSinceLastStatusMsg'] = parseInt(conf.maxTimeSinceLastStatusMsg);
	delete conf.maxTimeSinceLastStatusMsg;

	return timeoutConf;
}

function extractSlackNotifier(conf){
	slackNotifierConf = {};

	slackNotifierConf['webhook_url'] = conf.webhook_url;
	delete conf.webhook_url;

	slackNotifierConf['icon'] = conf.icon;
	delete conf.icon;

	slackNotifierConf['bot_name'] = conf.bot_name;
	delete conf.bot_name;

	return slackNotifierConf;
}

function extractTelegramNotifier(conf){
	telegramNotifierConf = {};

	telegramNotifierConf['token'] = conf.token;
	delete conf.token;

	telegramNotifierConf['chat_id'] = conf.chat_id;
	delete conf.chat_id;

	return telegramNotifierConf;
}

function extractMailNotifier(conf){
	mailNotifierConf = {};

	mailNotifierConf['server'] = conf.server;
	delete conf.server;

	mailNotifierConf['user'] = conf.user;
	delete conf.user;

	mailNotifierConf['password'] = conf.password;
	delete conf.password;

	return mailNotifierConf;
}