import aqt
from anki.utils import stripHTML as strip_html  # Anki 2.1.49 doesn't have the new name
from aqt.qt import QDialog, QVBoxLayout, QDialogButtonBox, QListWidget, QLabel, qconnect


def get_delayed_message(delay):
    question = strip_html(delay.sibling.question())
    if len(question) > 30:
        question = question[:30] + "…"
    today = aqt.mw.col.sched.today
    interval = delay.sibling.ivl
    old_relative_due = delay.old_absolute_due - today
    new_relative_due = delay.new_absolute_due - today

    return f"{question} (interval: {interval} days, " \
           f"due: {old_relative_due} → {new_relative_due} days after today)"


# noinspection PyAttributeOutsideInit
class DelayAfterSyncDialog(QDialog):
    def __init__(self):
        super().__init__(aqt.mw)  # noqa
        aqt.mw.garbage_collect_on_dialog_finish(self)
        self.setWindowTitle("Delay siblings")
        self.resize(500, 300)
        self.create_interface()

    def create_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        label = QLabel("After sync, I found some siblings that "
                       "should have been delayed. Delay now?")
        layout.addWidget(label)

        self.list = QListWidget(self)
        layout.addWidget(self.list)  # noqa

        button_box = QDialogButtonBox(self)
        delay_button = button_box.addButton("Delay", QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        qconnect(delay_button.clicked, self.accept)
        qconnect(cancel_button.clicked, self.reject)
        layout.addWidget(button_box)  # noqa

    def set_delays(self, delays):
        self.list.clear()
        self.list.addItems(get_delayed_message(delay) for delay in delays)
