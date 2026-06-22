import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { ChatbotComponent } from './shared/chatbot/chatbot';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    ChatbotComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
  title = 'PetHouse';
}


