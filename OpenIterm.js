/* global Application, delay */

function run(argv) {

	if (argv.length === 0) {
		return;
	}

	var Terminal = Application('iTerm');
	var SystemEvents = Application('System Events');

	if(! Terminal.frontmost()) {
		Terminal.activate();
		delay(1);
	}

	SystemEvents.keystroke(
		"t",
		{using: "command down"}
	);

	var path = argv.join(' ');
	var currentTerminalSession = Terminal.currentWindow.currentSession;
	currentTerminalSession.write({text: 'echo ""'});
	currentTerminalSession.write({text: 'clear'});
	// currentTerminalSession.write({text: 'echo "to: ' + path + '"'});
	currentTerminalSession.write({text: 'cd ' + path + ' && clear'});
}
