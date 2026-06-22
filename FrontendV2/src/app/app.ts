import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { ChatbotComponent } from './shared/chatbot/chatbot';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    ChatbotComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('FrontendV2');
}