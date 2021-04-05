from django.core.exceptions import ValidationError
from django.db import models
from sudokugame.sudoku_core import solve, difficulties, unflatten_split, flatten_join
from django.contrib.auth.models import User


class Board(models.Model):
    DIFFICULTY_CHOICES = [(diff_key, diff_info['name']) for diff_key, diff_info in difficulties.items()]

    grid = models.CharField(max_length=81, unique=True)
    solution = models.CharField(max_length=81, unique=True)
    difficulty = models.CharField(max_length=1, null=True, choices=DIFFICULTY_CHOICES)
    postedDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Validate disjoint inheritance
        if ((self.difficulty is None and self.postedDate is None) or
                (self.difficulty is not None and self.postedDate is not None)):
            raise ValidationError("Exactly one of the fields: 'difficulty' and 'postedDate' must be null")

        if self.solution is None:
            try:
                # If this field was not already set, calculate it now.
                self.solution = flatten_join(solve(unflatten_split(self.grid)))
            except Exception as e:
                raise ValidationError(f"Invalid sudoku board: {e}")

        super(Board, self).save(*args, **kwargs)

    def is_normal_board(self):
        return self.difficulty is not None

    def is_daily_challenge_board(self):
        return self.postedDate is not None

    def get_board_type_str(self):
        return self.difficulty if self.is_normal_board() else 'DC'

    def __str__(self):
        board_type = self.difficulty if self.difficulty else "Daily Challenge"
        return f"Sudoku Board #{self.id} ({board_type})"


class Game(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    submissionDate = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['board', 'user'], name="Unique board and user")
        ]

    def __str__(self):
        return f"Game: {self.user} played {self.board} @ {self.submissionDate}"


# Make email a required field.
# Solution from https://stackoverflow.com/questions/49134831/django-make-user-email-required
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
