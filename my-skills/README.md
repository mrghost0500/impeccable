# My skills

Personal skill setup, kept apart from the impeccable product. Nothing in this folder is read by the
impeccable build.

- `website-design/` is the master skill. Ask for any website or UI design work, or type
  `/website-design <what you want>`, and it picks the lead skill and runs the stages in order.
- `setup-skills.sh` installs the master skill plus every skill it calls into `~/.claude/skills`:
  impeccable, design-taste-frontend, Emil Kowalski's 15 skills, and 25 of Matt Pocock's, which it uses for the engineering around the design.

To get all of them in every new cloud session, put this in the environment's setup script:

```bash
git clone --depth 1 -q -b claude/impeccable-design-skill-u13s8t \
  https://github.com/mrghost0500/impeccable /tmp/my-skills \
  && bash /tmp/my-skills/my-skills/setup-skills.sh
rm -rf /tmp/my-skills
```
