class AudioPlayerController():
    def __init__(self, audio_player):
        self.audio_player = audio_player

    def toggle_playing(self):
        if not self.audio_player.filepath:
            return
        if not self.audio_player.prevent_recursion:
            self.audio_player.toggle_other_file()
        self.audio_player.playing = not self.audio_player.playing
        if self.audio_player.playing:
            self.audio_player.play_and_pause_button.setText("Pause")
            self.audio_player.media_player.play()
        else:
            self.audio_player.play_and_pause_button.setText("Play")
            self.audio_player.media_player.pause()

    def toggle_other_file(self):
        players = [self.audio_player.main_window.input_player1, self.audio_player.main_window.input_player2]

        for player in players:
            player.prevent_recursion = True

        for player in players:
            if player.playing and self.audio_player != player:
                player.toggle_playing()

        for player in players:
            player.prevent_recursion = False