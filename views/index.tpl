<!DOCTYPE html>
<!DOCTYPE html>
<html>
	<head>
		<title>Experiment Framework</title>
		<link rel="stylesheet" href="/static/style.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script type="text/javascript" src="/static/script.js"></script>
	</head>
	<body>
		<section id="page_wrapper">
			<section id="nav_bar">
				<ul>
				<li><a href="#">Home</a></li>
				<li><a href="#">Link 1</a></li>
				<li><a href="#">Link 2</a></li>
				<li><a href="#">Link 3</a></li>
				</ul>
			</section>
			<section id="header">
				<h1>Experiment Framework</h1>
			</section>
			<section id="content">
				<h2>Experiment konfigurieren</h2>
				<form action="#" methdod="post" id="createConfigForm">
					<fieldset>
						<legend>General</legend>
						<span class="input_field">
							<label for="title">Title</label>
							<input type="text" name="title" id="title" placeholder="Type in experiment's title/topic">
						</span>
					</fieldset>
					<fieldset>
						<legend>Parameters</legend>
						<span id="params_fields"></span>
						<button type="button" class="add_field_button" id="add_param_field_button">Add parameter</button>
					</fieldset>
					<fieldset>
						<legend>Export</legend>
						<span class="input_field">
							<label for="csvFilename">CSV-Filename</label>
							<input id="csvFilename" type="text" name="csvFilename" placeholder="Type in filename of csv export file">
						</span>
						<span class="input_field">
							<label for="csvFields">CSV-Fields</label>
							<input id="csvFields" type="text" name="csvFields" placeholder="Type in csv fields (table columns, comma seperated), such as 'id, firstname, lastname, street, city'">
						</span>
					</fieldset>
					<fieldset>
						<legend>Timeout</legend>
						<span class="input_field">
							<label for="defaultTimeout">Default Timeout</label>
							<input id="defaultTimeout" type="text" name="defaultTimeout" placeholder="Type in time in seconds until when a single instance of a experiment series has to be terminated">
						</span>
						<span class="input_field">
							<label for="outputPattern">Status Message Pattern</label>
							<input id="outputPattern" type="text" name="outputPattern" placeholder="Type in alorithms status message pattern, such as Algorithm works fine!">
						</span>
						<span class="input_field">
							<label for="maxTimeSinceLastStatusMsg">Status Message dependent Timout</label>
							<input id="maxTimeSinceLastStatusMsg" type="text" name="maxTimeSinceLastStatusMsg" placeholder="Type in timespan in seconds in which an algorithm has to send defined status message again to be called alive">
						</span>
					</fieldset>
					<fieldset>
						<legend>Slack-Notifier</legend>
						<span class="input_field">
							<label for="webhook_url">Webhook-URL</label>
							<input id="webhook_url" type="text" name="webhook_url" placeholder="Paste in your personal slack webhook">
						</span>
						<span class="input_field">
							<label for="icon">Bot-Chat-Icon</label>
							<input id="icon" type="text" name="icon" placeholder="Such as ':golf:'">
						</span>
						<span class="input_field">
							<label for="bot_name">Bot-Chat-Name</label>
							<input id="bot_name" type="text" name="bot_name" placeholder="Type in bot's chat name">
						</span>
					</fieldset>
					<fieldset>
						<legend>Telegram-Notifier</legend>
						<span class="input_field">
							<label for="token">Token</label>
							<input id="token" type="text" name="token" placeholder="Paste in your generated token for your created bot">
						</span>
						<span class="input_field">
							<label for="chat_id">Chat ID</label>
							<input id="chat_id" type="text" name="chat_id" placeholder="Paste in your telegram's chat id">
						</span>
					</fieldset>
					<fieldset>
						<legend>Mail-Notifier</legend>
						<span class="input_field">
							<label for="server">Server</label>
							<input id="server" type="text" name="server" placeholder="Type in mail server, such as 'smtp.gmail.com'">
						</span>
						<span class="input_field">
							<label for="user">User</label>
							<input id="user" type="text" name="user" placeholder="Type in your mail server's username">
						</span>
						<span class="input_field">
							<label for="password">Password</label>
							<input id="password" type="password" name="password" placeholder="Type in your password related to given username">
						</span>
					</fieldset>
					<button type="submit" class="submit_button">Generate Config-JSON Files &amp; Run Experiment</button>
				</form>
			</section>
			<section id="footer">

			</section>
		</section>
	</body>
</html>