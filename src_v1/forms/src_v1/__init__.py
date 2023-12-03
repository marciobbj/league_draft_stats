from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class BlueDraft(FlaskForm):
    top = SelectField(
        "top".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )
    mid = SelectField(
        "mid".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )
    jungle = SelectField(
        "jungle".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )
    adc = SelectField("ADC", choices=[], validators=[DataRequired()], coerce=str)
    support = SelectField(
        "support".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )

    def set_choices(self, champions):
        choices = list(
            set(
                [(champion["champion"], champion["champion"]) for champion in champions]
            )
        )
        self.top.choices = choices
        self.mid.choices = choices
        self.jungle.choices = choices
        self.adc.choices = choices
        self.support.choices = choices


class RedDraft(FlaskForm):
    top = SelectField(
        "top".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )
    mid = SelectField(
        "mid".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )
    jungle = SelectField(
        "jungle".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )
    adc = SelectField("ADC", choices=[], validators=[DataRequired()], coerce=str)
    support = SelectField(
        "support".capitalize(), choices=[], validators=[DataRequired()], coerce=str
    )

    def set_choices(self, champions):
        choices = list(
            set(
                [(champion["champion"], champion["champion"]) for champion in champions]
            )
        )
        self.top.choices = choices
        self.mid.choices = choices
        self.jungle.choices = choices
        self.adc.choices = choices
        self.support.choices = choices
