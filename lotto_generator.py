import argparse


CATEGORY_ADVICE = {
    "fashion": "사이즈, 착용감, 교환 정책을 상세페이지 상단에 배치하세요.",
    "beauty": "성분, 피부 타입, 사용 전후 이미지를 구조화하세요.",
    "food": "원산지, 보관법, 배송 마감 시간을 명확히 보여주세요.",
    "living": "공간별 사용 예시와 실측 이미지를 강화하세요.",
    "digital": "호환 기기, 보증, 설치 난이도를 표로 정리하세요.",
}


def diagnose_store(category, visitors, orders, average_order_value, ad_spend, reviews, rating):
    sales = orders * average_order_value
    conversion = (orders / visitors * 100) if visitors else 0
    roas = (sales / ad_spend) if ad_spend else (99 if sales else 0)
    trust_score = min(100, round((reviews * 0.9) + (rating * 12)))

    score = 40
    score += min(25, conversion * 5)
    score += min(20, roas * 2)
    score += min(15, trust_score / 6)
    score = max(0, min(100, round(score)))

    if score >= 82:
        priority = "확장 운영 우선"
    elif score >= 65:
        priority = "전환 개선 우선"
    else:
        priority = "기초 정비 우선"

    recommendations = []
    if conversion < 2:
        recommendations.append("상세페이지 첫 화면에 고객 문제, 사용 결과, 가격 혜택을 순서대로 보여주세요.")
    else:
        recommendations.append("전환율은 기본선을 넘었습니다. 잘 팔리는 옵션을 대표 이미지와 상품명에 반영하세요.")

    if roas < 4:
        recommendations.append("성과 낮은 광고 키워드는 중단하고 구매 전환 검색어 중심으로 재편하세요.")
    else:
        recommendations.append("광고 효율이 양호합니다. 전환 키워드별로 예산을 15-20%씩 증액하세요.")

    if trust_score < 60:
        recommendations.append("배송 완료 2일 뒤 포토리뷰 혜택을 안내해 리뷰 신뢰도를 보강하세요.")

    recommendations.append(CATEGORY_ADVICE.get(category, CATEGORY_ADVICE["living"]))

    return {
        "score": score,
        "priority": priority,
        "sales": sales,
        "conversion": conversion,
        "roas": roas,
        "trust_score": trust_score,
        "recommendations": recommendations,
    }


def main():
    parser = argparse.ArgumentParser(description="Naver Smart Store consulting diagnosis")
    parser.add_argument("--category", choices=sorted(CATEGORY_ADVICE), default="living")
    parser.add_argument("--visitors", type=int, default=3200)
    parser.add_argument("--orders", type=int, default=96)
    parser.add_argument("--aov", type=int, default=38000, help="average order value")
    parser.add_argument("--ad-spend", type=int, default=420000)
    parser.add_argument("--reviews", type=int, default=48)
    parser.add_argument("--rating", type=float, default=4.6)
    args = parser.parse_args()

    report = diagnose_store(
        args.category,
        args.visitors,
        args.orders,
        args.aov,
        args.ad_spend,
        args.reviews,
        args.rating,
    )

    print("네이버 스마트스토어 컨설팅 진단")
    print(f"점수: {report['score']}점")
    print(f"우선순위: {report['priority']}")
    print(f"예상 매출: {report['sales']:,}원")
    print(f"전환율: {report['conversion']:.1f}%")
    print(f"광고 매출 배수: {report['roas']:.1f}x")
    print(f"리뷰 신뢰도 점수: {report['trust_score']}점")
    print("추천 액션:")
    for index, recommendation in enumerate(report["recommendations"], start=1):
        print(f"{index}. {recommendation}")


if __name__ == "__main__":
    main()
