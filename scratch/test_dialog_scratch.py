import os
os.environ['KIVY_HEADLESS'] = '1'
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivy.clock import Clock

class TestApp(MDApp):
    def build(self):
        self.tf = MDTextField(MDTextFieldHintText(text='Enter playlist name'))
        self.dialog = MDDialog(
            MDDialogHeadlineText(text='New Playlist'),
            MDDialogContentContainer(self.tf, orientation='vertical'),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text='Cancel'), style='text'),
                MDButton(MDButtonText(text='Create'), style='text'),
            )
        )
        Clock.schedule_once(lambda dt: self.stop(), 0.5)
        return self.dialog

if __name__ == '__main__':
    TestApp().run()
    print("Dialog test completed successfully!")
