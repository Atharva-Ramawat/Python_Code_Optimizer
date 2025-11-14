const vscode = require('vscode');
const axios = require('axios');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

    console.log('"auto-code-optimizer" is now active!');

    let disposable = vscode.commands.registerCommand('auto-code-optimizer.optimize', async function () {
        
        // --- 1. Get the active text editor ---
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found.');
            return;
        }

        // --- 2. Get the selected code ---
        const selection = editor.selection; 
        const code = editor.document.getText(selection);
        
        if (code.length === 0) {
            vscode.window.showErrorMessage('No code selected. Please select the code you want to optimize.');
            return;
        }

        vscode.window.showInformationMessage('Sending code to optimizer...');

        // --- 3. Send the code to your Python server ---
        try {
            // This is your Cloud Server URL (it stays the same)
            const serverUrl = 'https://athv-auto-code-optimizer.hf.space/optimize';

            // --- THIS IS THE "EXPERT" PROMPT FOR GEMINI ---
            const prompt = `
You are an expert Python code optimizer.
Your task is to rewrite the provided code snippet to be more efficient and Pythonic.
Return ONLY the rewritten code, without any extra explanation or comments.

Original Code:
${code}

Optimized Code:
`;
            
            const response = await axios.post(serverUrl, {
                code: prompt // Send the new prompt
            });

            // --- 4. Get the response and REPLACE the code ---
            if (response.data && response.data.optimization) {
                const optimizedCode = response.data.optimization;
                
                await editor.edit(editBuilder => {
                    editBuilder.replace(selection, optimizedCode);
                });

                // Auto-format the new code
                await vscode.commands.executeCommand('editor.action.formatSelection');

            } else {
                vscode.window.showErrorMessage('Error: Received an invalid response from the server.');
            }

        } catch (error) {
            console.error(error);
            vscode.window.showErrorMessage('Failed to connect to the Gemini server. Is it running?');
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}