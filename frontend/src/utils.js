import GapFilling from "@/questions/GapFilling.vue";
import ListeningParaphrase from "@/questions/ListeningParaphrase.vue";
import ListeningConversation from "@/questions/ListeningConversation.vue";
import ListeningPassage from "@/questions/ListeningPassage.vue";
import ReadingLong from "@/questions/ReadingLong.vue";
import ReadingShort from "@/questions/ReadingShort.vue";
import Completion from "@/questions/Completion.vue";
import Synonym from "@/questions/Synonym.vue";
import Antonym from "@/questions/Antonym.vue";

export const mapping={
    "完形填空":GapFilling,
    "释义听力":ListeningParaphrase,
    "对话听力":ListeningConversation,
    "短篇听力":ListeningPassage,
    "长篇阅读":ReadingLong,
    "短篇阅读":ReadingShort,
    "首字母填空":Completion,
    "近义词":Synonym,
    "反义词":Antonym
}