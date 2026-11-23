import json
import os
import re
import time
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from vocational.models import (
    TradeCategory,
    TradeCourse,
    TradeGlossaryTerm,
    TradeLesson,
    TradeModule,
)

TARGET_LANGS = ("fr", "ig", "sw", "ar", "es", "pt")

PROTECTED_TOKENS = [
    "SO-DIMM",
    "CCTV",
    "NVMe",
    "MPPT",
    "RJ45",
    "OLED",
    "PoE",
    "NVR",
    "PWM",
    "VOC",
    "BMS",
    "ESD",
    "PPE",
    "QR",
    "AC/DC",
    "MC4",
    "MCB",
    "SPD",
    "IPA",
    "LAN",
    "BNC",
    "USB",
    "SATA",
    "RAM",
    "SSD",
]

CATEGORY_MAP = {
    "barbing-hairdressing-makeup-nail-art": {
        "fr": (
            "Coiffure, Barbier, Maquillage & Nail Art",
            "Formation pratique en coiffure, taille de barbe, maquillage professionnel et pose d'ongles avec protocoles d'hygiène et sécurité.",
        ),
        "ig": (
            "Ịkpụ Isi, Mmezi Ntutu, Makeup & Nail Art",
            "Ọzụzụ aka maka ịkpụ isi, ịhazi ntutu, ịchọ mma ihu, na ịrụ mbọ aka/ụkwụ tinyere ịdị ọcha na nchekwa.",
        ),
        "sw": (
            "Unyozi, Ususi wa Nywele, Vipodozi & Kucha",
            "Mafunzo ya vitendo ya unyozi, utengenezaji nywele, urembo wa uso, na kucha pamoja na taratibu za usafi na usalama.",
        ),
        "ar": (
            "الحلاقة وتصفيف الشعر والمكياج وفن الأظافر",
            "تدريب عملي في الحلاقة وتصفيف الشعر والمكياج وفن الأظافر مع معايير التعقيم والسلامة المهنية.",
        ),
        "es": (
            "Barbería, Peluquería, Maquillaje y Arte en Uñas",
            "Capacitación práctica en barbería, peluquería, maquillaje y manicura con protocolos de higiene y seguridad.",
        ),
        "pt": (
            "Barbearia, Cabeleireiro, Maquiagem e Nail Art",
            "Treinamento prático em barbearia, cabelo, maquiagem e unhas com protocolos de higiene e segurança.",
        ),
    },
    "cctv-intercom-network-installation": {
        "fr": (
            "Installation CCTV, Interphone & Réseau",
            "Installation pratique de caméras CCTV, systèmes d'interphone, câblage réseau et tests terrain pour sites résidentiels et commerciaux.",
        ),
        "ig": (
            "Nrụnye CCTV, Interkọm & Netwọk",
            "Ọzụzụ nrụnye igwe CCTV, interkọm, na eriri netwọk yana nnwale nchekwa maka ụlọ na azụmahịa.",
        ),
        "sw": (
            "Usakinishaji wa CCTV, Interkom & Mtandao",
            "Mafunzo ya vitendo ya kufunga kamera za CCTV, interkom, nyaya za mtandao, na upimaji wa mfumo.",
        ),
        "ar": (
            "تركيب أنظمة المراقبة CCTV والإنتركوم والشبكات",
            "تدريب عملي على تركيب كاميرات المراقبة وأنظمة الإنتركوم وتمديد الكابلات واختبار الشبكات.",
        ),
        "es": (
            "Instalación de CCTV, Intercomunicador y Red",
            "Capacitación práctica en instalación de cámaras CCTV, intercomunicadores, cableado de red y pruebas en campo.",
        ),
        "pt": (
            "Instalação de CFTV, Interfone e Rede",
            "Treinamento prático em instalação de câmeras CFTV, interfones, cabeamento de rede e testes em campo.",
        ),
    },
    "laptop-pc-hardware-repair": {
        "fr": (
            "Réparation Matérielle PC Portable & Bureau",
            "Diagnostic, maintenance préventive, remplacement de composants et sécurité ESD pour ordinateurs portables et fixes.",
        ),
        "ig": (
            "Nrụzi Ngwaike Laptọọpụ & Kọmpụta Desktọọpụ",
            "Nchọpụta nsogbu, nhicha, nnọchi ngwa, na nchekwa ESD maka laptọọpụ na kọmpụta desktọọpụ.",
        ),
        "sw": (
            "Ukarabati wa Vifaa vya Laptopu na Kompyuta",
            "Utambuzi wa hitilafu, usafishaji, ubadilishaji wa vipuri, na usalama wa ESD kwa laptopu na kompyuta za mezani.",
        ),
        "ar": (
            "صيانة مكونات اللابتوب وأجهزة الكمبيوتر المكتبية",
            "تشخيص الأعطال والصيانة الوقائية واستبدال القطع والالتزام بإجراءات الحماية من التفريغ الكهروستاتيكي ESD.",
        ),
        "es": (
            "Reparación de Hardware de Laptop y PC",
            "Diagnóstico, mantenimiento preventivo, reemplazo de componentes y seguridad ESD en laptops y computadoras de escritorio.",
        ),
        "pt": (
            "Reparo de Hardware de Notebook e PC",
            "Diagnóstico, manutenção preventiva, troca de componentes e segurança ESD em notebooks e desktops.",
        ),
    },
    "smartphone-repair": {
        "fr": (
            "Réparation Matérielle & Logicielle Smartphone",
            "Prise en charge atelier, sécurité ESD, remplacement d'écrans et batteries, diagnostic d'alimentation et restauration logicielle.",
        ),
        "ig": (
            "Nrụzi Ngwaike & Sọftụwia Ekwentị",
            "Nchekwa ESD, nnọchi ihuenyo na batrị, nyocha ọkụ, na nhazi sọftụwia ekwentị smart.",
        ),
        "sw": (
            "Ukarabati wa Vifaa na Programu za Simu",
            "Usalama wa ESD, ubadilishaji wa vioo na betri, upimaji wa umeme, na utatuzi wa programu za simu janja.",
        ),
        "ar": (
            "صيانة الهواتف الذكية برمجياً ومادياً",
            "سلامة ورشة العمل وحماية ESD واستبدال الشاشات والبطاريات وفحص الطاقة وحل مشاكل النظام.",
        ),
        "es": (
            "Reparación de Hardware y Software de Smartphones",
            "Seguridad ESD, cambio de pantallas y baterías, diagnóstico de energía y solução de fallos de software en teléfonos.",
        ),
        "pt": (
            "Reparo de Hardware e Software de Smartphones",
            "Segurança ESD, troca de telas e baterias, diagnóstico de energia e correção de falhas de software.",
        ),
    },
    "solar-renewable-energy": {
        "fr": (
            "Énergie Solaire & Énergies Renouvelables",
            "Audit de site, dimensionnement de charges, câblage PV, régulateurs MPPT/PWM, batteries et onduleurs hors réseau en toute sécurité.",
        ),
        "ig": (
            "Ike Anyanwụ (Solar) & Ike Mmeghari Ọhụrụ",
            "Nyocha ebe nrụnye, ngụkọta ike, njikọ panel anyanwụ, njikwa MPPT/PWM, batrị, na inveta.",
        ),
        "sw": (
            "Nishati ya Jua (Solar) na Mbadala",
            "Ukaguzi wa eneo, ukadiriaji wa mzigo wa umeme, nyaya za solar, vidhibiti vya MPPT/PWM, betri, na inveta.",
        ),
        "ar": (
            "الطاقة الشمسية والطاقات المتجددة",
            "معاينة الموقع وحساب الأحمال وتمديد الألواح الشمسية ومنظمات MPPT/PWM والبطاريات والعاكسات بأمان.",
        ),
        "es": (
            "Energía Solar y Energías Renovables",
            "Estudio de sitio, cálculo de cargas, cableado fotovoltaico, controladores MPPT/PWM, baterías e inversores aislados.",
        ),
        "pt": (
            "Energia Solar e Energias Renováveis",
            "Vistoria de local, dimensionamento de carga, cabeamento solar, controladores MPPT/PWM, baterias e inversores.",
        ),
    },
}

TIER_LABELS = {
    "tier_1": {
        "fr": "Niveau 1 : Fondamentaux & Sécurité",
        "ig": "Ọkwa 1: Ntọala & Nchekwa",
        "sw": "Kiwango cha 1: Msingi & Usalama",
        "ar": "المستوى 1: الأساسيات والسلامة",
        "es": "Nivel 1: Fundamentos y Seguridad",
        "pt": "Nível 1: Fundamentos e Segurança",
    },
    "tier_2": {
        "fr": "Niveau 2 : Maîtrise Pratique",
        "ig": "Ọkwa 2: Nkà Ọrụ Bara Uru",
        "sw": "Kiwango cha 2: Ustadi wa Vitendo",
        "ar": "المستوى 2: الإتقان العملي",
        "es": "Nivel 2: Dominio Práctico",
        "pt": "Nível 2: Domínio Prático",
    },
    "tier_3": {
        "fr": "Niveau 3 : Expertise Professionnelle",
        "ig": "Ọkwa 3: Ọkachamara & Asambodo",
        "sw": "Kiwango cha 3: Utaalamu & Cheti",
        "ar": "المستوى 3: الاحتراف والشهادة",
        "es": "Nivel 3: Maestría Profissional",
        "pt": "Nível 3: Maestria Profissional",
    },
}


def _offline_dictionary_path() -> str:
    base_dir = getattr(settings, "BASE_DIR", os.getcwd())
    return os.path.join(base_dir, "vocational", "data", "offline_translations.json")


def _load_offline_dictionary() -> dict[str, dict[str, str]]:
    path = _offline_dictionary_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, dict) else {}


def _protect_tokens(text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}
    protected = text
    for idx, token in enumerate(PROTECTED_TOKENS):
        pattern = re.compile(rf"\b{re.escape(token)}\b")
        if pattern.search(protected):
            key = f"__TOK{idx}__"
            placeholders[key] = token
            protected = pattern.sub(key, protected)
    return protected, placeholders


def _restore_tokens(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for key, token in placeholders.items():
        restored = restored.replace(key, token)
    return restored


def _translate_online(text: str, target_lang: str) -> str | None:
    protected, placeholders = _protect_tokens(text)
    chunks = []
    max_len = 1400
    remaining = protected
    while remaining:
        if len(remaining) <= max_len:
            part = remaining
            remaining = ""
        else:
            cut = remaining.rfind("\n", 0, max_len)
            if cut < 200:
                cut = remaining.rfind(" ", 0, max_len)
            if cut <= 0:
                cut = max_len
            part = remaining[:cut]
            remaining = remaining[cut:].lstrip()

        query = urllib.parse.urlencode(
            {
                "client": "gtx",
                "sl": "en",
                "tl": target_lang,
                "dt": "t",
                "q": part,
            }
        )
        url = f"https://translate.googleapis.com/translate_a/single?{query}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated_part = "".join(item[0] for item in data[0] if item and item[0])
            chunks.append(translated_part)

    joined = "\n".join(chunks) if len(chunks) > 1 else (chunks[0] if chunks else "")
    return _restore_tokens(joined, placeholders) if joined else None


def _translate_text(
    text: str,
    target_lang: str,
    online: bool,
    cache: dict[tuple[str, str], str],
    offline_dict: dict[str, dict[str, str]],
) -> str:
    if not text or not text.strip():
        return text
    cache_key = (target_lang, text)
    if cache_key in cache:
        return cache[cache_key]

    result = None

    # 1. Check bundled offline dictionary first
    dict_entry = offline_dict.get(text)
    if isinstance(dict_entry, dict):
        candidate = dict_entry.get(target_lang)
        if candidate and candidate.strip() and candidate != text:
            result = candidate

    # 2. Only try online endpoint if explicitly requested
    if not result and online:
        try:
            result = _translate_online(text, target_lang)
        except Exception:
            result = None

    if not result:
        result = text

    cache[cache_key] = result
    return result


class Command(BaseCommand):
    help = "Syncs _en fields and populates translated vocational content offline-first across fr, ig, sw, ar, es, and pt."

    def add_arguments(self, parser):
        parser.add_argument(
            "--lang",
            nargs="+",
            choices=list(TARGET_LANGS),
            default=list(TARGET_LANGS),
            help="Target language codes to populate (default: all 6 non-English languages).",
        )
        parser.add_argument(
            "--model",
            choices=["all", "categories", "courses", "modules", "lessons", "glossary"],
            default="all",
            help="Restrict translation pass to a single model group (default: all).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Max number of pending records to translate per model group in this run (0 = no limit).",
        )
        parser.add_argument(
            "--online",
            action="store_true",
            help="Opt in to online translation via Google Translate endpoint (not recommended for offline/low-power runs).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite already populated target language fields.",
        )
        parser.add_argument(
            "--skip-identical",
            action="store_true",
            help="Re-translate fields whose target value is currently identical to the _en fallback.",
        )
        parser.add_argument(
            "--sleep",
            type=float,
            default=0.1,
            help="Pause in seconds between online translation calls (default: 0.1).",
        )

    def _sync_en_and_translate_model(
        self,
        label,
        queryset,
        fields,
        langs,
        online,
        force,
        skip_identical,
        limit,
        sleep_sec,
        cache,
        offline_dict,
        custom_fn=None,
    ):
        updated_rows = 0
        pending_remaining = 0

        for obj in queryset:
            changed = False

            for field in fields:
                base_val = getattr(obj, field, None)
                en_field = f"{field}_en"
                en_val = getattr(obj, en_field, None)
                if base_val and not en_val:
                    setattr(obj, en_field, base_val)
                    changed = True

            needs_translation = False
            for lang in langs:
                for field in fields:
                    source_val = getattr(obj, f"{field}_en", None) or getattr(obj, field, None)
                    if not source_val:
                        continue
                    current_val = getattr(obj, f"{field}_{lang}", None)
                    if not current_val or force or (skip_identical and current_val == source_val):
                        needs_translation = True
                        break
                if needs_translation:
                    break

            if needs_translation and limit > 0 and updated_rows >= limit:
                if changed:
                    obj.save()
                pending_remaining += 1
                continue

            for lang in langs:
                for field in fields:
                    source_val = getattr(obj, f"{field}_en", None) or getattr(obj, field, None)
                    if not source_val:
                        continue

                    target_field = f"{field}_{lang}"
                    current_val = getattr(obj, target_field, None)
                    should_run = (
                        not current_val
                        or force
                        or (skip_identical and current_val == source_val)
                    )
                    if not should_run:
                        continue

                    custom_val = custom_fn(obj, field, lang) if custom_fn else None
                    if custom_val:
                        setattr(obj, target_field, custom_val)
                        changed = True
                    else:
                        translated = _translate_text(
                            source_val,
                            lang,
                            online=online,
                            cache=cache,
                            offline_dict=offline_dict,
                        )
                        if translated != current_val:
                            setattr(obj, target_field, translated)
                            changed = True
                        if online and sleep_sec > 0:
                            time.sleep(sleep_sec)

            if changed:
                obj.save()
                updated_rows += 1
                self.stdout.write(f"  [{label}] saved record #{updated_rows} (id={obj.pk})")

        return updated_rows, pending_remaining

    def handle(self, *args, **options):
        langs = options["lang"]
        model_choice = options["model"]
        limit = options["limit"]
        online = options["online"]
        force = options["force"]
        skip_identical = options["skip_identical"]
        sleep_sec = options["sleep"]
        cache: dict[tuple[str, str], str] = {}
        offline_dict = _load_offline_dictionary()

        results = {}

        with translation.override("en"):
            if model_choice in ("all", "categories"):
                results["categories"] = self._sync_en_and_translate_model(
                    "categories",
                    TradeCategory.objects.all().order_by("id"),
                    ["name", "description"],
                    langs,
                    online,
                    force,
                    skip_identical,
                    limit,
                    sleep_sec,
                    cache,
                    offline_dict,
                    custom_fn=lambda obj, field, lang: (
                        CATEGORY_MAP[obj.slug][lang][0]
                        if obj.slug in CATEGORY_MAP and field == "name"
                        else CATEGORY_MAP[obj.slug][lang][1]
                        if obj.slug in CATEGORY_MAP and field == "description"
                        else None
                    ),
                )

            if model_choice in ("all", "courses"):
                results["courses"] = self._sync_en_and_translate_model(
                    "courses",
                    TradeCourse.objects.select_related("category").all().order_by("id"),
                    [
                        "title",
                        "description",
                        "credential_awarded",
                        "required_tools",
                        "safety_guidelines",
                        "field_tips_summary",
                        "course_glossary_overview",
                    ],
                    langs,
                    online,
                    force,
                    skip_identical,
                    limit,
                    sleep_sec,
                    cache,
                    offline_dict,
                    custom_fn=lambda obj, field, lang: (
                        f"{CATEGORY_MAP[obj.category.slug][lang][0]} — {TIER_LABELS[obj.tier][lang]}"
                        if field == "title"
                        and obj.category
                        and obj.category.slug in CATEGORY_MAP
                        and obj.tier in TIER_LABELS
                        else None
                    ),
                )

            if model_choice in ("all", "modules"):
                results["modules"] = self._sync_en_and_translate_model(
                    "modules",
                    TradeModule.objects.all().order_by("id"),
                    ["title", "summary"],
                    langs,
                    online,
                    force,
                    skip_identical,
                    limit,
                    sleep_sec,
                    cache,
                    offline_dict,
                )

            if model_choice in ("all", "lessons"):
                results["lessons"] = self._sync_en_and_translate_model(
                    "lessons",
                    TradeLesson.objects.all().order_by("id"),
                    [
                        "title",
                        "learning_objectives",
                        "why_it_matters",
                        "core_explanation",
                        "step_by_step_field_guide",
                        "safety_and_traps",
                        "diagram_or_visual_guide",
                        "real_life_scenario",
                        "practice_activity",
                        "checkpoint_questions",
                    ],
                    langs,
                    online,
                    force,
                    skip_identical,
                    limit,
                    sleep_sec,
                    cache,
                    offline_dict,
                )

            if model_choice in ("all", "glossary"):
                results["glossary"] = self._sync_en_and_translate_model(
                    "glossary",
                    TradeGlossaryTerm.objects.all().order_by("id"),
                    ["term", "full_expansion", "definition", "field_application"],
                    langs,
                    online,
                    force,
                    skip_identical,
                    limit,
                    sleep_sec,
                    cache,
                    offline_dict,
                )

        summary = ", ".join(
            f"{k}: updated={v[0]} (remaining={v[1]})" for k, v in results.items()
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Translation sync complete for {langs} (online={online}): {summary}."
            )
        )